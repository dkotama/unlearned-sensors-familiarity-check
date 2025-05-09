#!/usr/bin/env python3
"""
Module for loading official sensor datasheets from markdown files.
"""

import os
import logging
import pandas as pd

class OfficialDatasheetLoader:
    """Class to load official sensor datasheets from local markdown files."""
    
    def __init__(self, sensors_csv_path, datasheet_directory='datasheet'):
        """Initialize the datasheet loader.
        
        Args:
            sensors_csv_path (str): Path to the CSV file containing sensor information
            datasheet_directory (str): Path to directory containing markdown datasheet files
        """
        self.sensors_csv_path = sensors_csv_path
        self.datasheet_directory = datasheet_directory
        self.logger = logging.getLogger(__name__)
    
    def get_official_datasheet(self, brand, sensor_type):
        """Get the official datasheet text for a given sensor.
        
        Args:
            brand (str): The brand of the sensor
            sensor_type (str): The type/model of the sensor
            
        Returns:
            tuple: (status, content) where status is a string ('Found', 'Not Found', etc.)
                  and content is the datasheet text if available
        """
        # Construct expected datasheet filename
        filename = f"{brand}_{sensor_type}.md"
        file_path = os.path.join(self.datasheet_directory, filename)
        
        # Check if file exists
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.logger.info(f"Successfully loaded datasheet from {file_path}")
                return "Found", content
            except Exception as e:
                self.logger.error(f"Error reading datasheet file {file_path}: {str(e)}")
                return "Error Reading", ""
        else:
            self.logger.warning(f"No datasheet file found for {brand} {sensor_type} at {file_path}")
            return "Not Found", ""