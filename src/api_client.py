"""
API client for communicating with various LLM providers.
"""

import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai
import time
import random
import concurrent.futures
import logging

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables for API keys
load_dotenv()

# Initialize global rate limiter
_rate_limiter = None

def get_rate_limiter(config):
    """Get or create the global rate limiter instance"""
    global _rate_limiter
    if _rate_limiter is None:
        # Import here to avoid circular imports
        from src.rate_limiter import RateLimiter
        _rate_limiter = RateLimiter(config)
    return _rate_limiter

class APIClient:
    """Base interface for API clients."""
    def __init__(self):
        self.rate_limiter = None
        self.provider_name = None
        
    def set_rate_limiter(self, rate_limiter):
        """Set the rate limiter for this client"""
        self.rate_limiter = rate_limiter
        
    def send_request(self, model, prompt):
        """
        Send a prompt to the specified model.
        
        Args:
            model (str): Model identifier
            prompt (str): The prompt text to send
            
        Returns:
            dict: Response data including text and token counts
            
        Raises:
            Exception: If the API request fails
        """
        raise NotImplementedError
        
    def _apply_rate_limiting(self, model):
        """Apply rate limiting before making an API request"""
        if self.rate_limiter and self.provider_name:
            return self.rate_limiter.wait_if_needed(self.provider_name, model)
        return 0

class OpenRouterClient(APIClient):
    def __init__(self, api_key, base_url, timeout=120):
        """
        Initialize the OpenRouter client.
        
        Args:
            api_key (str): API key for OpenRouter
            base_url (str): Base URL for OpenRouter API
            timeout (int): Request timeout in seconds
        """
        super().__init__()
        self.provider_name = "openrouter"
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        logger.info(f"OpenRouterClient initialized with base_url: {base_url}, timeout: {timeout}")
    
    def send_request(self, model, prompt):
        """
        Send a prompt to the specified model via OpenRouter API.
        
        Args:
            model (str): Model identifier (e.g., "openai/gpt-4")
            prompt (str): The prompt text to send
            
        Returns:
            dict: Response data including text and token counts
            
        Raises:
            Exception: If the API request fails
        """
        # Apply rate limiting
        wait_time = self._apply_rate_limiting(model)
        if wait_time > 0:
            logger.info(f"OpenRouter - Rate limited: waited {wait_time:.2f}s before sending request for {model}")
        
        endpoint = f"{self.base_url}/chat/completions"
        
        is_claude_model = 'anthropic' in model.lower() or 'claude' in model.lower()
        effective_timeout = self.timeout * 3 if is_claude_model else self.timeout
        
        logger.info(f"OpenRouter - Starting API request to {endpoint} for model: {model}")
        logger.info(f"OpenRouter - Model identified as Claude: {is_claude_model}, using timeout: {effective_timeout}s")
        logger.info(f"OpenRouter - Prompt length: {len(prompt)} characters")
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False,
            **({"temperature": 0.1, "top_p": 0.9} if is_claude_model else {})
        }
        
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                start_time = time.time()
                logger.info(f"OpenRouter - Sending request at {datetime.now().isoformat()} (attempt {retry_count+1}/{max_retries})")
                
                response = requests.post(
                    endpoint,
                    headers=self.headers,
                    data=json.dumps(payload),
                    timeout=effective_timeout
                )
                
                elapsed_time = time.time() - start_time
                logger.info(f"OpenRouter - Response received in {elapsed_time:.2f} seconds with status code: {response.status_code}")
                
                # Handle rate limiting errors (HTTP 429)
                if response.status_code == 429:
                    retry_count += 1
                    
                    # Try to extract rate limit information
                    try:
                        error_data = response.json()
                        headers = error_data.get("metadata", {}).get("headers", {})
                        if headers and "X-RateLimit-Limit" in headers:
                            rpm = int(headers["X-RateLimit-Limit"])
                            if self.rate_limiter:
                                self.rate_limiter.update_rate_limit(model, rpm)
                                logger.info(f"OpenRouter - Updated rate limit for {model} to {rpm} rpm based on API response")
                    except Exception as e:
                        logger.warning(f"OpenRouter - Error parsing rate limit information: {str(e)}")
                    
                    # Calculate backoff with jitter
                    backoff = min(60, (2 ** retry_count) + random.uniform(0, 1))
                    logger.warning(f"OpenRouter - Rate limit exceeded for {model}. Retrying in {backoff:.2f}s (attempt {retry_count}/{max_retries})")
                    time.sleep(backoff)
                    continue
                
                # For other errors, just raise
                response.raise_for_status()
                response_json = response.json()
                
                # Handle different response formats
                if "choices" in response_json and len(response_json["choices"]) > 0:
                    text = response_json["choices"][0]["message"]["content"]
                elif "output" in response_json:
                    text = response_json["output"]
                else:
                    logger.warning(f"OpenRouter - Unrecognized response structure: {response_json}")
                    text = json.dumps(response_json)  # Fallback to raw JSON string
                
                result = {
                    "text": text,
                    "input_tokens": response_json.get("usage", {}).get("prompt_tokens", 0),
                    "output_tokens": response_json.get("usage", {}).get("completion_tokens", 0)
                }
                
                logger.info(f"OpenRouter - Request successful. Input tokens: {result['input_tokens']}, Output tokens: {result['output_tokens']}")
                logger.info(f"OpenRouter - Response length: {len(result['text'])} characters")
                
                return result
            
            except requests.exceptions.Timeout:
                if retry_count < max_retries - 1:
                    retry_count += 1
                    backoff = min(60, (2 ** retry_count) + random.uniform(0, 1))
                    logger.warning(f"OpenRouter - Request timed out. Retrying in {backoff:.2f}s (attempt {retry_count}/{max_retries})")
                    time.sleep(backoff)
                else:
                    logger.error(f"OpenRouter - Request timed out after {effective_timeout} seconds for model {model} (all retries exhausted)")
                    raise Exception(f"API request to OpenRouter timed out after {effective_timeout} seconds. For Claude models, consider increasing the timeout in your config.")
            except requests.exceptions.RequestException as e:
                if retry_count < max_retries - 1 and (hasattr(e, 'response') and e.response is not None and e.response.status_code >= 500):
                    # Retry on server errors
                    retry_count += 1
                    backoff = min(60, (2 ** retry_count) + random.uniform(0, 1))
                    logger.warning(f"OpenRouter - Server error {e.response.status_code}. Retrying in {backoff:.2f}s (attempt {retry_count}/{max_retries})")
                    time.sleep(backoff)
                else:
                    error_msg = f"API request failed: {str(e)}"
                    if hasattr(e, 'response') and e.response is not None:
                        error_msg += f" Response: {e.response.text}"
                        logger.error(f"OpenRouter - Request failed with status {e.response.status_code}: {e.response.text}")
                    else:
                        logger.error(f"OpenRouter - Request failed: {str(e)}")
                    raise Exception(error_msg)

class GeminiClient(APIClient):
    def __init__(self, api_key, timeout=120):
        """
        Initialize the Gemini client using the correct Google Gen AI SDK structure.
        
        Args:
            api_key (str): Direct API key for Gemini
            timeout (int): Request timeout in seconds
        """
        super().__init__()
        self.provider_name = "google_gemini"
        self.api_key = api_key
        if not self.api_key:
            raise Exception("Gemini API key is not provided in configuration")
        self.timeout = timeout
        
        # Configure the API key globally instead of creating a client instance
        genai.configure(api_key=self.api_key)
        logger.info(f"GeminiClient initialized with timeout: {timeout}")
    
    def send_request(self, model, prompt):
        """
        Send a prompt to the specified Gemini model with retry mechanism.
        
        Args:
            model (str): Model identifier (e.g., "google/gemini-2.5-pro-exp-03-25")
            prompt (str): The prompt text to send
            
        Returns:
            dict: Response data including text and token counts
            
        Raises:
            Exception: If the API request fails after retries
        """
        # Apply rate limiting
        wait_time = self._apply_rate_limiting(model)
        if wait_time > 0:
            logger.info(f"Gemini - Rate limited: waited {wait_time:.2f}s before sending request for {model}")
            
        max_retries = 3
        # Extract model name from full identifier if needed (e.g., "google/gemini-pro" -> "gemini-pro")
        model_name = model.split('/')[-1]
        logger.info(f"Gemini - Starting API request for model: {model}")
        logger.info(f"Gemini - Prompt length: {len(prompt)} characters")
        logger.info(f"Gemini - Using model name: {model_name}")
        
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                logger.info(f"Gemini - Attempt {attempt+1}/{max_retries} at {datetime.now().isoformat()}")
                
                # Create a GenerativeModel instance
                gen_model = genai.GenerativeModel(model_name)
                
                # Define generation config using the appropriate structure
                generation_config = {
                    "temperature": 0.7,
                    "max_output_tokens": 8192,
                    "top_p": 0.95,
                    "top_k": 40
                }
                
                # Define request options including SDK-level timeout
                request_options = {"timeout": self.timeout}
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    logger.info(f"Gemini - Submitting request to thread executor with SDK timeout: {self.timeout}s")
                    # Use generate_content with the appropriate parameters
                    future = executor.submit(
                        gen_model.generate_content, 
                        prompt,
                        generation_config=generation_config,
                        request_options=request_options
                    )
                    
                    try:
                        # Using a slightly longer timeout for the overall operation
                        overall_timeout = self.timeout * 1.1  # 10% buffer
                        logger.info(f"Gemini - Waiting for response (overall timeout: {overall_timeout:.1f}s)")
                        response = future.result(timeout=overall_timeout)
                        elapsed_time = time.time() - start_time
                        logger.info(f"Gemini - Response received in {elapsed_time:.2f} seconds")
                    except concurrent.futures.TimeoutError:
                        logger.error(f"Gemini - Request timed out after {overall_timeout:.1f} seconds for model {model}")
                        future.cancel()  # Attempt to cancel the background task
                        raise Exception(f"API request to Gemini timed out after {overall_timeout:.1f} seconds for model {model}")
                
                # Count tokens for the prompt if available
                try:
                    # Use countTokens method if available
                    token_count = gen_model.count_tokens(prompt)
                    input_tokens = token_count.total_tokens
                    logger.info(f"Gemini - Input tokens counted: {input_tokens}")
                except Exception as e:
                    logger.warning(f"Gemini - Failed to count tokens: {str(e)}")
                    input_tokens = 0
                
                # Extract text from response
                if hasattr(response, 'text'):
                    response_text = response.text
                elif hasattr(response, 'parts') and response.parts:
                    response_text = response.parts[0].text
                else:
                    response_text = str(response)
                
                # Create result object
                result = {
                    "text": response_text,
                    "input_tokens": input_tokens,
                    "output_tokens": getattr(response, "candidates_token_count", 0)
                }
                
                logger.info(f"Gemini - Request successful. Input tokens: {result['input_tokens']}, Output tokens: {result['output_tokens']}")
                logger.info(f"Gemini - Response length: {len(result['text'])} characters")
                
                return result
                
            except Exception as e:
                error_str = str(e).lower()
                # Handle rate limiting
                if "rate limit" in error_str or "quota" in error_str or "429" in error_str:
                    # Try to extract rate limit information from error message
                    try:
                        import re
                        # Look for patterns like "limited to X requests per minute"
                        rpm_pattern = r"limited to (\d+) requests? per minute"
                        rpm_match = re.search(rpm_pattern, error_str)
                        if rpm_match and self.rate_limiter:
                            rpm = int(rpm_match.group(1))
                            self.rate_limiter.update_rate_limit(model, rpm)
                            logger.info(f"Gemini - Updated rate limit for {model} to {rpm} rpm based on error message")
                    except Exception as ex:
                        logger.warning(f"Gemini - Error parsing rate limit information: {str(ex)}")
                    
                    # Apply exponential backoff
                    if attempt < max_retries - 1:
                        delay = (2 ** (attempt + 1)) + random.uniform(0, 1)  # More aggressive backoff for rate limits
                        logger.warning(f"Gemini - Rate limit exceeded. Retrying in {delay:.2f} seconds (attempt {attempt+1}/{max_retries})...")
                        time.sleep(delay)
                        continue
                
                # Special handling for deadline exceeded errors
                if "deadline exceeded" in error_str or "deadline_exceeded" in error_str:
                    logger.warning(f"Gemini - API deadline exceeded (attempt {attempt+1}/{max_retries})")
                
                logger.error(f"Gemini - API request failed (attempt {attempt+1}/{max_retries}): {type(e).__name__} - {str(e)} for model {model}")
                if attempt == max_retries - 1:
                    logger.error(f"Gemini - All retry attempts exhausted. Giving up.")
                    raise Exception(f"API request to Gemini failed after {max_retries} attempts: {str(e)}")
                
                # Exponential backoff with jitter for other errors
                delay = (2 ** attempt) + random.uniform(0, 1)  # Increased jitter for better distribution
                logger.info(f"Gemini - Retrying in {delay:.2f} seconds...")
                time.sleep(delay)

    def stream_request(self, model, prompt):
        """
        Stream a request to the Gemini API.
        
        Args:
            model (str): The model identifier to use.
            prompt: The prompt text to send to the model.
            
        Yields:
            Chunks of the response as they arrive.
        """
        try:
            start_time = time.time()
            logger.info(f"Gemini - Starting stream request at {datetime.now().isoformat()}")
            
            # Extract model name from full identifier if needed
            model_name = model.split('/')[-1]
            
            # Create GenerativeModel instance
            gen_model = genai.GenerativeModel(model_name)
            
            # Configure generation parameters
            generation_config = {
                "temperature": 0.7,
                "max_output_tokens": 8192,
                "top_p": 0.95,
                "top_k": 40
            }
            
            # Use the streaming interface 
            response = gen_model.generate_content(
                prompt,
                generation_config=generation_config,
                stream=True
            )
            
            for chunk in response:
                if hasattr(chunk, 'text'):
                    yield chunk.text
                elif hasattr(chunk, 'parts') and chunk.parts:
                    yield chunk.parts[0].text
                else:
                    yield str(chunk)
                
            response_time = time.time() - start_time
            logger.info(f"Gemini streaming request completed in {response_time:.2f}s")
            
        except Exception as e:
            logger.error(f"Error during streaming: {str(e)}")
            yield f"Error: {str(e)}"

class APIClientFactory:
    @staticmethod
    def get_client(provider_config, provider_name, config=None):
        """
        Factory method to get the appropriate API client based on provider.
        
        Args:
            provider_config (dict): Configuration for the provider
            provider_name (str): Name of the provider
            config (dict, optional): Full application config for rate limiting
            
        Returns:
            APIClient: Instance of the appropriate client
        """
        logger.info(f"Creating API client for provider: {provider_name}")
        
        try:
            client = None
            
            if provider_name == "openrouter":
                if 'api_key' not in provider_config or not provider_config['api_key']:
                    logger.error("OpenRouter API key missing or empty in provider_config")
                    raise ValueError("OpenRouter API key is required")
                    
                if 'base_url' not in provider_config or not provider_config['base_url']:
                    logger.error("OpenRouter base_url missing or empty in provider_config")
                    raise ValueError("OpenRouter base URL is required")
                    
                timeout = provider_config.get('timeout', 120)
                logger.info(f"Creating OpenRouterClient with base_url: {provider_config['base_url']}, timeout: {timeout}")
                
                client = OpenRouterClient(
                    provider_config['api_key'],
                    provider_config['base_url'],
                    timeout
                )
            elif provider_name == "google_gemini":
                if 'api_key' not in provider_config or not provider_config['api_key']:
                    logger.error("Gemini API key missing or empty in provider_config")
                    raise ValueError("Gemini API key is required")
                    
                timeout = provider_config.get('timeout', 120)
                logger.info(f"Creating GeminiClient with timeout: {timeout}")
                
                client = GeminiClient(
                    provider_config['api_key'],
                    timeout
                )
            else:
                logger.error(f"Unsupported provider: {provider_name}")
                raise ValueError(f"Unsupported provider: {provider_name}")
            
            # Set rate limiter if config is provided
            if config and client:
                rate_limiter = get_rate_limiter(config)
                client.set_rate_limiter(rate_limiter)
                logger.info(f"Rate limiter configured for {provider_name} client")
                
            return client
        except Exception as e:
            logger.error(f"Error creating API client for provider {provider_name}: {str(e)}")
            raise