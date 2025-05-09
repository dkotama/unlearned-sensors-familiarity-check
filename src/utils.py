#!/usr/bin/env python3
"""
Utility functions for the LLM review system.
"""

import json
import re
import logging
import os
from datetime import datetime

logger = logging.getLogger(__name__)

# Configure a special logger for raw LLM responses
response_logger = logging.getLogger('review_responses')
response_logger.setLevel(logging.DEBUG)

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Set up a file handler for the response logger
response_file_handler = logging.FileHandler('logs/review_responses.log')
response_file_handler.setLevel(logging.DEBUG)
response_formatter = logging.Formatter('%(asctime)s - %(message)s')
response_file_handler.setFormatter(response_formatter)
response_logger.addHandler(response_file_handler)

def extract_json_from_llm_response(response_text, sensor_info=None, model_info=None):
    """Extract JSON data from an LLM response with multiple fallback methods.
    
    Args:
        response_text (str): The raw response text from the LLM
        sensor_info (str, optional): Sensor information for logging
        model_info (str, optional): Model information for logging
        
    Returns:
        tuple: (scores_dict, justifications_dict, error_message)
    """
    # Log the raw response for debugging
    context_info = f"[{sensor_info} - {model_info}]" if sensor_info and model_info else ""
    response_logger.debug(f"{context_info} Raw LLM Response:\n{response_text}\n{'-'*80}")
    
    if not response_text or not isinstance(response_text, str):
        return {}, {}, "Empty or invalid response"
    
    # Check if response is an error message (which happens with some providers)
    if '"error"' in response_text:
        try:
            # Try to parse the error JSON
            error_json = json.loads(response_text)
            if 'error' in error_json:
                error_msg = f"API error: {json.dumps(error_json['error'])}"
                response_logger.error(f"{context_info} {error_msg}")
                return {}, {}, error_msg
        except json.JSONDecodeError:
            # If we can't parse it, continue with normal processing
            pass
    
    # Initialize return values
    scores_dict = {}
    justifications_dict = {}
    error_message = None
    
    # METHOD 1: Try to extract JSON from code blocks
    json_match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', response_text)
    if json_match:
        try:
            json_str = json_match.group(1).strip()
            response_logger.debug(f"{context_info} Found JSON in code block:\n{json_str}")
            data = json.loads(json_str)
            scores_dict, justifications_dict = _normalize_json_data(data)
            return scores_dict, justifications_dict, None
        except json.JSONDecodeError as e:
            error_message = f"Failed to parse JSON from code block: {e}"
            response_logger.warning(f"{context_info} {error_message}")
    
    # METHOD 2: Try to extract raw JSON object
    json_match = re.search(r'\{[\s\S]*?\}', response_text)
    if json_match:
        try:
            json_str = json_match.group(0).strip()
            response_logger.debug(f"{context_info} Found raw JSON:\n{json_str}")
            data = json.loads(json_str)
            scores_dict, justifications_dict = _normalize_json_data(data)
            return scores_dict, justifications_dict, None
        except json.JSONDecodeError as e:
            error_message = f"Failed to parse raw JSON: {e}"
            response_logger.warning(f"{context_info} {error_message}")
    
    # METHOD 3: Try regex pattern matching for key-value pairs
    try:
        # Extract scores using patterns like "P1 Score: 4" or "P1: 4"
        score_pattern = r'([pP](\d+)|[oO]verall)[\s_]*(?:[sS]core)?:?\s*(\d+)'
        score_matches = re.findall(score_pattern, response_text)
        
        for match in score_matches:
            key = match[0].upper() if match[0].lower() != "overall" else "Overall"
            if key.upper().startswith("P"):
                key = f"P{match[1]}"
            scores_dict[key] = int(match[2])
        
        # Extract justifications with a more flexible pattern
        just_sections = re.split(r'([pP]\d+|[oO]verall)[\s_]*[jJ]ustification', response_text)
        if len(just_sections) > 1:
            for i in range(1, len(just_sections), 2):
                if i + 1 < len(just_sections):
                    key = just_sections[i].strip().upper()
                    if key.upper().startswith("P"):
                        # Extract the number from P1, P2, etc.
                        key = f"P{key[1:]}" if len(key) > 1 else "P1"
                    elif key.lower() == "overall":
                        key = "Overall"
                    value = just_sections[i+1].split('\n')[0].strip(':, ')
                    justifications_dict[key] = value
        
        if scores_dict:
            error_message = "Used regex pattern matching as fallback" if error_message else None
            response_logger.info(f"{context_info} Extracted data using regex: scores={scores_dict}, justifications={justifications_dict}")
            return scores_dict, justifications_dict, error_message
            
    except Exception as e:
        error_message = f"Failed in regex pattern matching: {e}"
        response_logger.warning(f"{context_info} {error_message}")
    
    # If we get here, all methods failed
    error_message = error_message or "Failed to extract any review data"
    response_logger.error(f"{context_info} All parsing methods failed: {error_message}")
    return {}, {}, error_message

def _normalize_json_data(data):
    """Normalize the JSON data returned by the LLM to standard format.
    
    Args:
        data (dict): The parsed JSON data from the LLM
        
    Returns:
        tuple: (scores_dict, justifications_dict)
    """
    scores = {}
    justifications = {}
    
    # Look for scores under various possible key formats
    for i in range(1, 17):
        # Define possible variations of score keys
        p_key = f"P{i}"
        p_key_lower = f"p{i}"
        possible_score_keys = [
            f"{p_key}_score", f"{p_key_lower}_score", 
            f"p{i}_score", p_key, p_key_lower,
            f"score_{p_key}", f"score_{p_key_lower}",
            f"score_p{i}"
        ]
        
        # Define possible variations of justification keys
        possible_just_keys = [
            f"{p_key}_justification", f"{p_key_lower}_justification",
            f"p{i}_justification", f"{p_key}_just", f"{p_key_lower}_just",
            f"justification_{p_key}", f"justification_{p_key_lower}",
            f"justification_p{i}", f"p{i}_reasoning", f"p{i}_explanation"
        ]
        
        # Find the first matching key for score
        for key in possible_score_keys:
            if key in data:
                scores[p_key] = data[key]
                break
        
        # Find the first matching key for justification
        for key in possible_just_keys:
            if key in data:
                justifications[p_key] = data[key]
                break
    
    # Handle overall score similarly
    overall_score_keys = ["overall_score", "Overall_score", "Overall", "overall", "OVERALL"]
    for key in overall_score_keys:
        if key in data:
            scores["Overall"] = data[key]
            break
    
    # Handle overall justification
    overall_just_keys = ["overall_justification", "Overall_justification", "overall_just", 
                         "Overall_just", "overall_reasoning", "overall_explanation"]
    for key in overall_just_keys:
        if key in data:
            justifications["Overall"] = data[key]
            break
    
    return scores, justifications