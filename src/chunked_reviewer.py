import os
import json
import logging
import time
import traceback
from pathlib import Path

from pydantic import ValidationError
from src.review_models import ReviewChunk1, ReviewChunk2, ReviewChunk3, CompleteReview

class ChunkedReviewer:
    def __init__(self, review_client, config, logger=None):
        """Initialize a chunked reviewer that splits reviews into manageable parts"""
        self.client = review_client
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        
        # Get and validate path configuration
        self.base_prompt_path = config.get('review_prompt_template_path')
        self.reviews_path = config.get('reviews_base_path', 'results/reviews/')
        
        # Try multiple potential paths for official datasheets
        self.official_datasheets_path = config.get('official_datasheets_path', 'data/official_datasheets/')
        self.alternate_paths = [
            'datasheet/',               # Root datasheet folder
            'data/official_datasheets/', # Config specified path
            'data/datasheets/',         # Another common location
            'datasheets/'               # Another possibility
        ]
        
        # Ensure directories exist
        os.makedirs(self.reviews_path, exist_ok=True)
        
        # Log initialization
        self.logger.info(f"ChunkedReviewer initialized with:")
        self.logger.info(f"  - Prompt template: {self.base_prompt_path}")
        self.logger.info(f"  - Reviews output: {self.reviews_path}")
        self.logger.info(f"  - Primary datasheets path: {self.official_datasheets_path}")
        self.logger.info(f"  - Will check alternate paths if needed: {self.alternate_paths}")
    
    def create_chunk_prompt(self, chunk_num, sensor_brand, sensor_model, generated_datasheet, official_datasheet):
        """Create a prompt for a specific chunk of the review"""
        # Read base prompt
        try:
            with open(self.base_prompt_path, 'r') as f:
                template = f.read()
                
            # Replace general placeholders
            prompt = template.replace("{{SENSOR_BRAND}}", sensor_brand)
            prompt = prompt.replace("{{SENSOR_MODEL}}", sensor_model)
            prompt = prompt.replace("{{generated_datasheet}}", generated_datasheet)
            prompt = prompt.replace("{{official_datasheet}}", official_datasheet)
            
            # Modify for specific chunk
            if chunk_num == 1:
                prompt = self._modify_prompt_for_chunk1(prompt)
            elif chunk_num == 2:
                prompt = self._modify_prompt_for_chunk2(prompt)
            elif chunk_num == 3:
                prompt = self._modify_prompt_for_chunk3(prompt)
                
            self.logger.info(f"Created prompt for chunk {chunk_num}, length: {len(prompt)} characters")
            return prompt
            
        except FileNotFoundError:
            self.logger.error(f"Review prompt template not found at {self.base_prompt_path}")
            raise
        except Exception as e:
            self.logger.error(f"Error creating chunk prompt: {str(e)}")
            self.logger.error(traceback.format_exc())
            raise
    
    def _modify_prompt_for_chunk1(self, prompt):
        """Modify prompt to focus on P1-P6 criteria only"""
        # Add specific instructions for this chunk
        chunk_instructions = """
# IMPORTANT: Response Format for CHUNK 1
This is part 1 of 3 of the review. ONLY evaluate criteria P1-P6 (Disclaimer through Potential Applications).
Return ONLY valid JSON with this exact structure:

```json
{
  "sensor_evaluated": "BRAND MODEL",
  "p1_score": 5,
  "p1_justification": "Brief justification for P1",
  "p2_score": 4,
  "p2_justification": "Brief justification for P2",
  "p3_score": 4,
  "p3_justification": "Brief justification for P3",
  "p4_score": 5,
  "p4_justification": "Brief justification for P4",
  "p5_score": 3,
  "p5_justification": "Brief justification for P5",
  "p6_score": 4,
  "p6_justification": "Brief justification for P6"
}
```

DO NOT include evaluations for P7-P16 or overall score in this response.
Keep justifications concise (under 100 characters) to ensure response fits within API limits.
"""
        return prompt + chunk_instructions
    
    def _modify_prompt_for_chunk2(self, prompt):
        """Modify prompt to focus on P7-P11 criteria only"""
        chunk_instructions = """
# IMPORTANT: Response Format for CHUNK 2
This is part 2 of 3 of the review. ONLY evaluate criteria P7-P11 (Pin Configuration through Sensor Performance).
Return ONLY valid JSON with this exact structure:

```json
{
  "sensor_evaluated": "BRAND MODEL",
  "p7_score": 4,
  "p7_justification": "Brief justification for P7",
  "p8_score": 5,
  "p8_justification": "Brief justification for P8",
  "p9_score": 3,
  "p9_justification": "Brief justification for P9",
  "p10_score": 4,
  "p10_justification": "Brief justification for P10",
  "p11_score": 5,
  "p11_justification": "Brief justification for P11"
}
```

DO NOT include evaluations for P1-P6, P12-P16, or overall score in this response.
Keep justifications concise (under 100 characters) to ensure response fits within API limits.
"""
        return prompt + chunk_instructions
    
    def _modify_prompt_for_chunk3(self, prompt):
        """Modify prompt to focus on P12-P16 criteria and overall score"""
        chunk_instructions = """
# IMPORTANT: Response Format for CHUNK 3
This is part 3 of 3 of the review. ONLY evaluate criteria P12-P16 (Communication Protocol through Compliance) and provide an overall score.
Return ONLY valid JSON with this exact structure:

```json
{
  "sensor_evaluated": "BRAND MODEL",
  "p12_score": 4,
  "p12_justification": "Brief justification for P12",
  "p13_score": 3,
  "p13_justification": "Brief justification for P13",
  "p14_score": 5,
  "p14_justification": "Brief justification for P14",
  "p15_score": 4,
  "p15_justification": "Brief justification for P15",
  "p16_score": "N/A",
  "p16_justification": "Brief justification for P16",
  "overall_score": 4,
  "overall_justification": "Brief overall justification",
  "confirmation": "This review is exclusively for the BRAND MODEL sensor and contains no references to other sensor models."
}
```

DO NOT include evaluations for P1-P11 in this response.
Keep justifications concise (under 100 characters) to ensure response fits within API limits.
"""
        return prompt + chunk_instructions
        
    def extract_json_from_response(self, response_text):
        """Extract JSON from the LLM response text"""
        try:
            # Try to find JSON block
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                json_content = response_text[json_start:json_end].strip()
            else:
                # Try to find JSON content directly
                json_content = response_text.strip()
                
                # Look for opening/closing braces if there's text before/after
                if not json_content.startswith('{'):
                    first_brace = json_content.find('{')
                    if first_brace >= 0:
                        json_content = json_content[first_brace:]
                
                if not json_content.endswith('}'):
                    last_brace = json_content.rfind('}')
                    if last_brace >= 0:
                        json_content = json_content[:last_brace+1]
            
            return json.loads(json_content)
        except Exception as e:
            self.logger.error(f"Failed to extract JSON: {e}")
            self.logger.debug(f"Raw response: {response_text[:500]}...")
            return None
            
    def process_review_chunk(self, chunk_num, model_id, sensor_brand, sensor_model, prompt):
        """Process a single review chunk"""
        try:
            self.logger.info(f"Processing {sensor_brand} {sensor_model} review chunk {chunk_num} with model {model_id}")
            
            # Use send_request method instead of generate_text
            response = self.client.send_request(model=model_id, prompt=prompt)
            
            # Extract text from response dictionary
            if isinstance(response, dict) and 'text' in response:
                response_text = response['text']
            else:
                response_text = str(response)
                
            json_data = self.extract_json_from_response(response_text)
            if not json_data:
                self.logger.error(f"Failed to extract JSON from chunk {chunk_num}")
                return None
                
            # Validate with appropriate Pydantic model
            if chunk_num == 1:
                return ReviewChunk1(**json_data)
            elif chunk_num == 2:
                return ReviewChunk2(**json_data)
            elif chunk_num == 3:
                return ReviewChunk3(**json_data)
                
        except ValidationError as e:
            self.logger.error(f"Validation error for chunk {chunk_num}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error processing chunk {chunk_num}: {e}")
            return None
    
    def combine_chunks(self, chunk1, chunk2, chunk3):
        """Combine three chunks into a complete review"""
        combined_data = {
            "sensor_evaluated": chunk1.sensor_evaluated,
            # Add fields from chunk 1 (P1-P6)
            "p1_score": chunk1.p1_score,
            "p1_justification": chunk1.p1_justification,
            "p2_score": chunk1.p2_score,
            "p2_justification": chunk1.p2_justification,
            "p3_score": chunk1.p3_score,
            "p3_justification": chunk1.p3_justification,
            "p4_score": chunk1.p4_score,
            "p4_justification": chunk1.p4_justification,
            "p5_score": chunk1.p5_score,
            "p5_justification": chunk1.p5_justification,
            "p6_score": chunk1.p6_score,
            "p6_justification": chunk1.p6_justification,
            # Add fields from chunk 2 (P7-P11)
            "p7_score": chunk2.p7_score,
            "p7_justification": chunk2.p7_justification,
            "p8_score": chunk2.p8_score,
            "p8_justification": chunk2.p8_justification,
            "p9_score": chunk2.p9_score,
            "p9_justification": chunk2.p9_justification,
            "p10_score": chunk2.p10_score,
            "p10_justification": chunk2.p10_justification,
            "p11_score": chunk2.p11_score,
            "p11_justification": chunk2.p11_justification,
            # Add fields from chunk 3 (P12-P16 + overall)
            "p12_score": chunk3.p12_score,
            "p12_justification": chunk3.p12_justification,
            "p13_score": chunk3.p13_score,
            "p13_justification": chunk3.p13_justification,
            "p14_score": chunk3.p14_score,
            "p14_justification": chunk3.p14_justification,
            "p15_score": chunk3.p15_score,
            "p15_justification": chunk3.p15_justification,
            "p16_score": chunk3.p16_score,
            "p16_justification": chunk3.p16_justification,
            "overall_score": chunk3.overall_score,
            "overall_justification": chunk3.overall_justification,
            "confirmation": chunk3.confirmation
        }
        
        return CompleteReview(**combined_data)
            
    def review_sensor(self, model_id, sensor_brand, sensor_model, generated_datasheet_path):
        """Process a complete sensor review by breaking it into chunks"""
        # Read the generated datasheet file
        try:
            self.logger.info(f"Reading generated datasheet from {generated_datasheet_path}")
            with open(generated_datasheet_path, 'r') as f:
                generated_datasheet = f.read()
            self.logger.info(f"Successfully read generated datasheet ({len(generated_datasheet)} chars)")
                
            # Try to locate and read the official datasheet with different file extensions
            official_datasheet = None
            official_datasheet_path = None
            
            # Try all possible paths to find the official datasheet
            for base_path in self.alternate_paths:
                # Try with .md extension first (most common)
                potential_path = os.path.join(base_path, f"{sensor_brand}_{sensor_model}.md")
                self.logger.info(f"Trying to load official datasheet from: {potential_path}")
                
                if os.path.exists(potential_path):
                    self.logger.info(f"Found official datasheet at {potential_path}")
                    with open(potential_path, 'r') as f:
                        official_datasheet = f.read()
                    official_datasheet_path = potential_path
                    break
                    
                # Try with .txt extension as fallback
                potential_path_txt = os.path.join(base_path, f"{sensor_brand}_{sensor_model}.txt") 
                if os.path.exists(potential_path_txt):
                    self.logger.info(f"Found official datasheet at {potential_path_txt}")
                    with open(potential_path_txt, 'r') as f:
                        official_datasheet = f.read()
                    official_datasheet_path = potential_path_txt
                    break
            
            if official_datasheet is None:
                self.logger.error(f"Official datasheet for {sensor_brand}_{sensor_model} not found in any of the searched paths")
                self.logger.error(f"Searched paths: {self.alternate_paths}")
                self.logger.error(f"Tried the following files:")
                for path in self.alternate_paths:
                    self.logger.error(f"  - {os.path.join(path, f'{sensor_brand}_{sensor_model}.md')}")
                    self.logger.error(f"  - {os.path.join(path, f'{sensor_brand}_{sensor_model}.txt')}")
                raise FileNotFoundError(f"Official datasheet for {sensor_brand}_{sensor_model} not found")
                
            self.logger.info(f"Successfully read official datasheet from {official_datasheet_path} ({len(official_datasheet)} chars)")
                
        except Exception as e:
            self.logger.error(f"Error reading datasheet files: {str(e)}")
            self.logger.error(traceback.format_exc())
            return None
            
        # Process each chunk with delay between to respect rate limits
        chunks = []
        for chunk_num in range(1, 4):
            try:
                prompt = self.create_chunk_prompt(
                    chunk_num, sensor_brand, sensor_model, 
                    generated_datasheet, official_datasheet
                )
                
                self.logger.info(f"Sending chunk {chunk_num} to LLM model {model_id}")
                chunk = self.process_review_chunk(
                    chunk_num, model_id, sensor_brand, sensor_model, prompt
                )
                
                if not chunk:
                    self.logger.error(f"Failed to process chunk {chunk_num}")
                    return None
                    
                self.logger.info(f"Successfully processed chunk {chunk_num}")
                chunks.append(chunk)
                
                # Add delay between chunks to respect rate limits
                if chunk_num < 3:
                    delay = 30
                    self.logger.info(f"Waiting {delay} seconds between chunks to respect rate limits")
                    time.sleep(delay)
            except Exception as e:
                self.logger.error(f"Error processing chunk {chunk_num}: {str(e)}")
                self.logger.error(traceback.format_exc())
                return None
                
        # Combine chunks into complete review
        try:
            self.logger.info(f"Combining {len(chunks)} chunks into complete review")
            complete_review = self.combine_chunks(chunks[0], chunks[1], chunks[2])
            
            # Save the review
            output_path = os.path.join(
                self.reviews_path,
                f"{model_id.replace('/', '_')}_{sensor_brand}_{sensor_model}_review.json"
            )
            
            self.logger.info(f"Saving review to {output_path}")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            with open(output_path, 'w') as f:
                f.write(complete_review.model_dump_json(indent=2))
                
            self.logger.info(f"Successfully saved complete review to {output_path}")
            return complete_review
            
        except Exception as e:
            self.logger.error(f"Error combining chunks: {str(e)}")
            self.logger.error(traceback.format_exc())
            return None