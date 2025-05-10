import time
import threading
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class RateLimiter:
    """
    Implements a token bucket rate limiter for API requests.
    Allows for model-specific rate limiting.
    """
    
    def __init__(self, config):
        """
        Initialize the rate limiter with configuration.
        
        Args:
            config (dict): Configuration dictionary containing rate limits
        """
        self.config = config
        self.provider_limits = {}
        self.model_limits = {}
        self.last_request_times = {}
        self.lock = threading.Lock()
        
        # Initialize provider rate limits
        for provider_name, provider_config in config.get('providers', {}).items():
            if 'rate_limit' in provider_config:
                rpm = provider_config['rate_limit'].get('requests_per_minute', 5)
                self.provider_limits[provider_name] = rpm
        
        # Initialize model-specific rate limits
        for model_id, rpm in config.get('model_rate_limits', {}).items():
            self.model_limits[model_id] = rpm
            self.last_request_times[model_id] = datetime.now() - timedelta(minutes=1)
    
    def wait_if_needed(self, provider_name, model_id):
        """
        Check if a request can be made or if we need to wait due to rate limits.
        Will block until the request can be made.
        
        Args:
            provider_name (str): The provider name (e.g., "openrouter", "google_gemini")
            model_id (str): The model ID (e.g., "google/gemini-2.5-pro-exp-03-25")
            
        Returns:
            float: The amount of time waited in seconds
        """
        with self.lock:
            # Check if we have a model-specific rate limit
            if model_id in self.model_limits:
                rpm = self.model_limits[model_id]
                wait_seconds = self._calculate_wait_time(model_id, rpm)
                
                if wait_seconds > 0:
                    logger.info(f"Rate limiting: waiting {wait_seconds:.2f}s for model {model_id} (limit: {rpm} rpm)")
                    time.sleep(wait_seconds)
                    self.last_request_times[model_id] = datetime.now()
                    return wait_seconds
                
                self.last_request_times[model_id] = datetime.now()
            
            # If no model-specific limit or no wait needed, check provider limit
            elif provider_name in self.provider_limits:
                rpm = self.provider_limits[provider_name]
                provider_key = f"provider_{provider_name}"
                
                if provider_key not in self.last_request_times:
                    self.last_request_times[provider_key] = datetime.now() - timedelta(minutes=1)
                
                wait_seconds = self._calculate_wait_time(provider_key, rpm)
                
                if wait_seconds > 0:
                    logger.info(f"Rate limiting: waiting {wait_seconds:.2f}s for provider {provider_name} (limit: {rpm} rpm)")
                    time.sleep(wait_seconds)
                    self.last_request_times[provider_key] = datetime.now()
                    return wait_seconds
                
                self.last_request_times[provider_key] = datetime.now()
            
        return 0
    
    def _calculate_wait_time(self, key, rpm):
        """
        Calculate how long to wait based on the last request time and rate limit.
        
        Args:
            key (str): The key to check in last_request_times
            rpm (int): Requests per minute limit
            
        Returns:
            float: Number of seconds to wait (0 if no wait needed)
        """
        if key not in self.last_request_times:
            return 0
            
        # Calculate seconds per request based on RPM
        seconds_per_request = 60.0 / rpm
        
        # Calculate time since last request
        time_since_last = (datetime.now() - self.last_request_times[key]).total_seconds()
        
        # If we need to wait, return the wait time
        if time_since_last < seconds_per_request:
            return seconds_per_request - time_since_last
            
        return 0
    
    def update_rate_limit(self, model_id, new_rpm):
        """
        Update the rate limit for a specific model based on API responses.
        Useful when receiving 429 responses with rate limit information.
        
        Args:
            model_id (str): The model ID to update
            new_rpm (int): The new requests per minute limit
        """
        with self.lock:
            self.model_limits[model_id] = new_rpm
            logger.info(f"Updated rate limit for {model_id} to {new_rpm} rpm")