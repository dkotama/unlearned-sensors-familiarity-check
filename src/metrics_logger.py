"""
Module for logging performance metrics of LLM responses.
"""

import os
import csv
from datetime import datetime

class MetricsLogger:
    def __init__(self, log_path):
        """
        Initialize the metrics logger.
        
        Args:
            log_path (str): Path to the CSV file for logging metrics
        """
        self.log_path = log_path
        # Ensure the directory exists
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        # Write header if file doesn't exist
        if not os.path.exists(log_path):
            with open(log_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'Timestamp', 'SensorBrand', 'SensorType', 'Model', 
                    'ResponseTimeSeconds', 'InputTokens', 'OutputTokens', 'ResponseLengthChars'
                ])
    
    def log_metrics(self, sensor_brand, sensor_type, model, response_time, input_tokens, output_tokens, response_length):
        """
        Log performance metrics for an LLM response.
        
        Args:
            sensor_brand (str): Brand of the sensor
            sensor_type (str): Type/model of the sensor
            model (str): Model identifier (e.g., "openai/gpt-4")
            response_time (float): Response time in seconds
            input_tokens (int): Number of input tokens
            output_tokens (int): Number of output tokens
            response_length (int): Length of response in characters
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp, sensor_brand, sensor_type, model, 
                response_time, input_tokens, output_tokens, response_length
            ])