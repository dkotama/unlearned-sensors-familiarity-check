#!/usr/bin/env python3
"""
Module for logging and managing LLM review scores.
"""

import os
import csv
import pandas as pd
import logging
from datetime import datetime

class ReviewScoreLogger:
    """Class to log and manage LLM review scores for datasheets."""

    P_CRITERIA_BASE_NAMES = [
        "Disclaimer", "Manufacturer_Info", "General_Description", "Theory_Of_Operation",
        "Features", "Potential_Applications", "Pin_Configuration", "Absolute_Maximum_Ratings",
        "Electrical_Characteristics", "Operating_Conditions", "Sensor_Performance",
        "Communication_Protocol", "Register_Map", "Package_Information", "Basic_Usage",
        "Compliance_Certifications"
    ]

    ORDERED_FIELD_NAMES = [
        'Sensor_Brand',
        'Sensor_Type',
        'Generated_Datasheet_LLM_Provider',
        'Generated_Datasheet_LLM_Model',
        'Reviewer_LLM_Provider',
        'Reviewer_LLM_Model',
        'Official_Datasheet_Status',
        'P1_Disclaimer_Score',
        'P2_Manufacturer_Info_Score',
        'P3_General_Description_Score',
        'P4_Theory_Of_Operation_Score',
        'P5_Features_Score',
        'P6_Potential_Applications_Score',
        'P7_Pin_Configuration_Score',
        'P8_Absolute_Maximum_Ratings_Score',
        'P9_Electrical_Characteristics_Score',
        'P10_Operating_Conditions_Score',
        'P11_Sensor_Performance_Score',
        'P12_Communication_Protocol_Score',
        'P13_Register_Map_Score',
        'P14_Package_Information_Score',
        'P15_Basic_Usage_Score',
        'P16_Compliance_Certifications_Score',
        'Average_Pn_Score',
        'Overall_Likert_Score',
        'P1_Disclaimer_Justification',
        'P2_Manufacturer_Info_Justification',
        'P3_General_Description_Justification',
        'P4_Theory_Of_Operation_Justification',
        'P5_Features_Justification',
        'P6_Potential_Applications_Justification',
        'P7_Pin_Configuration_Justification',
        'P8_Absolute_Maximum_Ratings_Justification',
        'P9_Electrical_Characteristics_Justification',
        'P10_Operating_Conditions_Justification',
        'P11_Sensor_Performance_Justification',
        'P12_Communication_Protocol_Justification',
        'P13_Register_Map_Justification',
        'P14_Package_Information_Justification',
        'P15_Basic_Usage_Justification',
        'P16_Compliance_Certifications_Justification',
        'Overall_Justification',
        'Review_Timestamp'
    ]
    
    def __init__(self, base_path):
        """Initialize the review score logger.
        
        Args:
            base_path (str): Base directory for storing review logs
        """
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)
        self.logger = logging.getLogger(__name__)
    
    def log_review(self, reviewer_provider, reviewer_model, sensor_brand, sensor_type, 
                   generator_provider, generator_model, official_datasheet_status, 
                   scores, justifications):
        """Log a review to the appropriate CSV file.
        
        Args:
            reviewer_provider (str): Provider of the reviewer LLM (e.g., 'google')
            reviewer_model (str): Model name of the reviewer LLM (e.g., 'gemini-1.5-pro')
            sensor_brand (str): Brand of the sensor being reviewed
            sensor_type (str): Type/model of the sensor being reviewed
            generator_provider (str): Provider of the LLM that generated the datasheet
            generator_model (str): Model name of the LLM that generated the datasheet
            official_datasheet_status (str): Status of official datasheet fetching
            scores (dict): Dictionary containing scores for each criteria
            justifications (dict): Dictionary containing justifications for each score
            
        Returns:
            str: Path to the CSV file where review was logged
        """
        # Create directory structure: reviews/[ReviewerLLMProvider]_[ReviewerLLMModel]/
        reviewer_dir = f"{reviewer_provider}_{reviewer_model}"
        review_dir = os.path.join(self.base_path, reviewer_dir)
        os.makedirs(review_dir, exist_ok=True)
        
        # CSV file path: [ReviewerLLMProvider]_[ReviewerLLMModel]/[SensorBrand]_[SensorType].csv
        sensor_filename = f"{sensor_brand}_{sensor_type}.csv".replace(" ", "_")
        csv_path = os.path.join(review_dir, sensor_filename)
        
        # Check if file exists to determine if we need to write headers
        file_exists = os.path.isfile(csv_path)
        
        # Prepare row data
        average_score = self._calculate_average_score(scores) # Assumes scores dict uses "P1", "P2", ... keys
        review_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        row_data = {
            'Sensor_Brand': sensor_brand,
            'Sensor_Type': sensor_type,
            'Generated_Datasheet_LLM_Provider': generator_provider,
            'Generated_Datasheet_LLM_Model': generator_model,
            'Reviewer_LLM_Provider': reviewer_provider,
            'Reviewer_LLM_Model': reviewer_model,
            'Official_Datasheet_Status': official_datasheet_status,
            'Average_Pn_Score': average_score,
            'Overall_Likert_Score': scores.get('Overall', 'N/A'),
            'Overall_Justification': justifications.get('Overall', ''),
            'Review_Timestamp': review_timestamp,
        }
        
        # Add individual Pn scores and justifications
        # scores and justifications dicts are expected to be keyed "P1", "P2", ..., "P16"
        for i, base_name in enumerate(self.P_CRITERIA_BASE_NAMES, 1):
            p_key = f"P{i}" # Key for accessing input scores/justifications dicts (e.g., "P1")
            
            score_col_name = f"P{i}_{base_name}_Score"
            just_col_name = f"P{i}_{base_name}_Justification"
            
            row_data[score_col_name] = scores.get(p_key, "N/A")
            row_data[just_col_name] = justifications.get(p_key, "")
            
        # Write to CSV
        with open(csv_path, 'a', newline='', encoding='utf-8') as f:
            csv_writer = csv.DictWriter(f, fieldnames=self.ORDERED_FIELD_NAMES)
            if not file_exists:
                csv_writer.writeheader()
            csv_writer.writerow(row_data)
        
        self.logger.info(f"Review for {sensor_brand} {sensor_type} logged to {csv_path}")
        return csv_path
    
    def _calculate_average_score(self, scores):
        """Calculate average score from P1-P16.
        
        Args:
            scores (dict): Dictionary of scores
            
        Returns:
            float or str: Average score or "N/A" if no valid scores
        """
        valid_scores = []
        for i in range(1, 17):
            key = f"P{i}"
            if key in scores and scores[key] != "N/A" and isinstance(scores[key], (int, float)):
                valid_scores.append(scores[key])
        
        if valid_scores:
            return sum(valid_scores) / len(valid_scores)
        return "N/A"
    
    def get_review_summary(self, reviewer_provider, reviewer_model):
        """Get a summary of reviews performed by a specific reviewer LLM.
        
        Args:
            reviewer_provider (str): Provider of the reviewer LLM
            reviewer_model (str): Model name of the reviewer LLM
            
        Returns:
            pandas.DataFrame or None: DataFrame with review summary or None if no data
        """
        reviewer_dir = f"{reviewer_provider}_{reviewer_model}"
        review_dir = os.path.join(self.base_path, reviewer_dir)
        
        if not os.path.exists(review_dir):
            self.logger.warning(f"No reviews found for {reviewer_provider} {reviewer_model}")
            return None
        
        # Find all CSV files in the directory
        csv_files = [f for f in os.listdir(review_dir) if f.endswith('.csv')]
        
        if not csv_files:
            self.logger.warning(f"No CSV files found in {review_dir}")
            return None
        
        # Read and concatenate all CSVs
        dfs = []
        for csv_file in csv_files:
            try:
                file_path = os.path.join(review_dir, csv_file)
                df = pd.read_csv(file_path)
                dfs.append(df)
            except Exception as e:
                self.logger.error(f"Error reading {csv_file}: {str(e)}")
        
        if not dfs:
            return None
        
        # Concatenate all DataFrames
        return pd.concat(dfs, ignore_index=True)