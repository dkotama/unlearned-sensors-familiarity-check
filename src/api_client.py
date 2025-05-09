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

class APIClient:
    """Base interface for API clients."""
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

class OpenRouterClient(APIClient):
    def __init__(self, api_key, base_url, timeout=120):
        """
        Initialize the OpenRouter client.
        
        Args:
            api_key (str): API key for OpenRouter
            base_url (str): Base URL for OpenRouter API
            timeout (int): Request timeout in seconds
        """
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
        
        try:
            start_time = time.time()
            logger.info(f"OpenRouter - Sending request at {datetime.now().isoformat()}")
            
            response = requests.post(
                endpoint,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=effective_timeout
            )
            
            elapsed_time = time.time() - start_time
            logger.info(f"OpenRouter - Response received in {elapsed_time:.2f} seconds with status code: {response.status_code}")
            
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
            logger.error(f"OpenRouter - Request timed out after {effective_timeout} seconds for model {model}")
            raise Exception(f"API request to OpenRouter timed out after {effective_timeout} seconds. For Claude models, consider increasing the timeout in your config.")
        except requests.exceptions.RequestException as e:
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
        Initialize the Gemini client.
        
        Args:
            api_key (str): Direct API key for Gemini
            timeout (int): Request timeout in seconds
        """
        self.api_key = api_key
        if not self.api_key:
            raise Exception("Gemini API key is not provided in configuration")
        self.timeout = timeout
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
        max_retries = 3
        model_name = model.split('/')[-1]
        logger.info(f"Gemini - Starting API request for model: {model}")
        logger.info(f"Gemini - Prompt length: {len(prompt)} characters")
        logger.info(f"Gemini - Using model name: {model_name}")
        
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                logger.info(f"Gemini - Attempt {attempt+1}/{max_retries} at {datetime.now().isoformat()}")
                
                gen_model = genai.GenerativeModel(model_name)
                logger.info(f"Gemini - GenerativeModel instance created")
                
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    logger.info(f"Gemini - Submitting request to thread executor with timeout: {self.timeout}s")
                    future = executor.submit(gen_model.generate_content, prompt)
                    
                    try:
                        logger.info(f"Gemini - Waiting for response (timeout: {self.timeout}s)")
                        response = future.result(timeout=self.timeout)
                        elapsed_time = time.time() - start_time
                        logger.info(f"Gemini - Response received in {elapsed_time:.2f} seconds")
                    except concurrent.futures.TimeoutError:
                        logger.error(f"Gemini - Request timed out after {self.timeout} seconds for model {model}")
                        raise Exception(f"API request to Gemini timed out after {self.timeout} seconds")
                
                # Extract relevant information
                has_usage_metadata = hasattr(response, 'usage_metadata')
                logger.info(f"Gemini - Response has usage metadata: {has_usage_metadata}")
                
                result = {
                    "text": response.text if hasattr(response, 'text') else response.candidates[0].content.parts[0].text,
                    "input_tokens": response.usage_metadata.prompt_token_count if has_usage_metadata else 0,
                    "output_tokens": response.usage_metadata.candidates_token_count if has_usage_metadata else 0
                }
                
                logger.info(f"Gemini - Request successful. Input tokens: {result['input_tokens']}, Output tokens: {result['output_tokens']}")
                logger.info(f"Gemini - Response length: {len(result['text'])} characters")
                
                return result
                
            except Exception as e:
                logger.error(f"Gemini - API request failed (attempt {attempt+1}/{max_retries}): {str(e)} for model {model}")
                if attempt == max_retries - 1:
                    logger.error(f"Gemini - All retry attempts exhausted. Giving up.")
                    raise Exception(f"API request to Gemini failed after {max_retries} attempts: {str(e)}")
                
                # Exponential backoff with jitter
                delay = (2 ** attempt) + random.uniform(0, 0.1)
                logger.info(f"Gemini - Retrying in {delay:.2f} seconds...")
                time.sleep(delay)

class APIClientFactory:
    @staticmethod
    def get_client(provider_config, provider_name):
        """
        Factory method to get the appropriate API client based on provider.
        
        Args:
            provider_config (dict): Configuration for the provider
            provider_name (str): Name of the provider
            
        Returns:
            APIClient: Instance of the appropriate client
        """
        logger.info(f"Creating API client for provider: {provider_name}")
        
        try:
            if provider_name == "openrouter":
                if 'api_key' not in provider_config or not provider_config['api_key']:
                    logger.error("OpenRouter API key missing or empty in provider_config")
                    raise ValueError("OpenRouter API key is required")
                    
                if 'base_url' not in provider_config or not provider_config['base_url']:
                    logger.error("OpenRouter base_url missing or empty in provider_config")
                    raise ValueError("OpenRouter base URL is required")
                    
                timeout = provider_config.get('timeout', 120)
                logger.info(f"Creating OpenRouterClient with base_url: {provider_config['base_url']}, timeout: {timeout}")
                
                return OpenRouterClient(
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
                
                return GeminiClient(
                    provider_config['api_key'],
                    timeout
                )
            else:
                logger.error(f"Unsupported provider: {provider_name}")
                raise ValueError(f"Unsupported provider: {provider_name}")
        except Exception as e:
            logger.error(f"Error creating API client for provider {provider_name}: {str(e)}")
            raise