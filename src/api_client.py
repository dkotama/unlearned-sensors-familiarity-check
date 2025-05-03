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
        
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False
        }
        
        try:
            response = requests.post(
                endpoint,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=self.timeout
            )
            
            response.raise_for_status()
            response_json = response.json()
            
            # Extract relevant information
            result = {
                "text": response_json["choices"][0]["message"]["content"],
                "input_tokens": response_json.get("usage", {}).get("prompt_tokens", 0),
                "output_tokens": response_json.get("usage", {}).get("completion_tokens", 0)
            }
            
            return result
            
        except requests.exceptions.RequestException as e:
            error_msg = f"API request failed: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_msg += f" Response: {e.response.text}"
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
        for attempt in range(max_retries):
            try:
                # Extract the model name after the provider prefix
                model_name = model.split('/')[-1]
                gen_model = genai.GenerativeModel(model_name)
                response = gen_model.generate_content(prompt)
                
                # Extract relevant information
                result = {
                    "text": response.text if hasattr(response, 'text') else response.candidates[0].content.parts[0].text,
                    "input_tokens": response.usage_metadata.prompt_token_count if hasattr(response, 'usage_metadata') else 0,
                    "output_tokens": response.usage_metadata.candidates_token_count if hasattr(response, 'usage_metadata') else 0
                }
                
                return result
                
            except Exception as e:
                error_msg = f"Gemini API request failed (attempt {attempt+1}/{max_retries}): {str(e)}"
                if attempt == max_retries - 1:
                    raise Exception(error_msg)
                # Exponential backoff with jitter
                delay = (2 ** attempt) + random.uniform(0, 0.1)
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
        if provider_name == "openrouter":
            return OpenRouterClient(
                provider_config['api_key'],
                provider_config['base_url'],
                provider_config.get('timeout', 120)
            )
        elif provider_name == "google_gemini":
            return GeminiClient(
                provider_config['api_key'],
                provider_config.get('timeout', 120)
            )
        else:
            raise Exception(f"Unsupported provider: {provider_name}")