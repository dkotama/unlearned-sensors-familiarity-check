"""
Module for processing and saving results from LLM responses.
"""

import os
from datetime import datetime

class ResultProcessor:
    def __init__(self, base_path):
        """
        Initialize the result processor.
        
        Args:
            base_path (str): Base directory path for saving results
        """
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)
    
    def save_result(self, sensor_brand, sensor_type, model, response_text):
        """
        Save the LLM response to a markdown file.
        
        Args:
            sensor_brand (str): Brand of the sensor
            sensor_type (str): Type/model of the sensor
            model (str): Model identifier (e.g., "openai/gpt-4")
            response_text (str): Response text from the LLM
            
        Returns:
            str: Path to the saved file
        """
        # Create a clean model name for the filename
        model_name = model.replace('/', '_')
        
        # Create sensor-specific directory
        sensor_dir = os.path.join(self.base_path, f"{sensor_brand}_{sensor_type}")
        if not os.path.exists(sensor_dir):
            os.makedirs(sensor_dir)
        
        # Create a timestamp for uniqueness
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Construct filename
        filename = f"{model_name}_{timestamp}.md"
        filepath = os.path.join(sensor_dir, filename)
        
        # Save the response
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(response_text)
            
        return filepath