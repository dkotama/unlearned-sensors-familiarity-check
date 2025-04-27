"""
Module for generating prompts from templates and sensor data.
"""

class PromptGenerator:
    def __init__(self, template_path):
        """
        Initialize the prompt generator with a template file.
        
        Args:
            template_path (str): Path to the prompt template file
        """
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = f.read()
    
    def generate_prompt(self, sensor_brand, sensor_type, datasheet_content):
        """
        Generate a prompt by filling the template with sensor data.
        
        Args:
            sensor_brand (str): Brand of the sensor
            sensor_type (str): Type/model of the sensor
            datasheet_content (str): Content of the datasheet
            
        Returns:
            str: Generated prompt text
        """
        return self.template.format(
            sensor_brand=sensor_brand,
            sensor_type=sensor_type,
            datasheet_content=datasheet_content
        )