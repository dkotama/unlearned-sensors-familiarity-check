"""
API client for communicating with OpenRouter to send prompts to various LLMs.
"""

import requests
import json
from datetime import datetime

class OpenRouterClient:
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