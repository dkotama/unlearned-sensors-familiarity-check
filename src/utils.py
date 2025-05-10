#!/usr/bin/env python3

"""
Utility functions for the sensor datasheet project.
Contains functions for extracting JSON from LLM responses, among others.
"""

import json
import re
import logging

logger = logging.getLogger(__name__)

def extract_json_from_llm_response(response_text, sensor_info=None, model_info=None):
    """
    Extract and parse JSON from LLM response text with robust error handling.
    
    Args:
        response_text (str): The raw text response from an LLM
        sensor_info (str, optional): Information about the sensor for error reporting
        model_info (str, optional): Information about the model for error reporting
        
    Returns:
        tuple: (scores_dict, justifications_dict, error_message)
            - scores_dict: Dictionary of scores
            - justifications_dict: Dictionary of justifications
            - error_message: Error message if any, None otherwise
    """
    if not response_text:
        return {}, {}, "Empty response received"
    
    # For debug identification
    context = f"sensor={sensor_info}, model={model_info}" if sensor_info and model_info else ""
    
    # Check for API errors first
    if "error" in response_text.lower() and ("rate limit" in response_text.lower() or 
                                           "api error" in response_text.lower() or
                                           "status code" in response_text.lower()):
        error_msg = f"API error: {response_text[:200]}..."
        return {}, {}, error_msg
        
    # Try to find a JSON block (with or without backticks)
    json_str = None
    error_msg = None
    
    # First attempt: Look for JSON code blocks
    if "```json" in response_text or "```" in response_text:
        try:
            # Try to extract from JSON-specific code block
            json_pattern = r"```json(.*?)```"
            matches = re.findall(json_pattern, response_text, re.DOTALL)
            
            if not matches:
                # Try generic code blocks
                json_pattern = r"```(.*?)```" 
                matches = re.findall(json_pattern, response_text, re.DOTALL)
                
            if matches:
                for potential_json in matches:
                    try:
                        parsed_json = json.loads(potential_json.strip())
                        json_str = potential_json.strip()
                        break
                    except:
                        continue
        except Exception as e:
            error_msg = f"Error extracting JSON from code blocks: {str(e)}"
    
    # Second attempt: Find everything between outermost braces if previous attempt failed
    if not json_str:
        try:
            brace_pattern = r"\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\}"
            matches = re.findall(brace_pattern, response_text)
            
            if matches:
                for potential_json in matches:
                    try:
                        parsed_json = json.loads(potential_json)
                        json_str = potential_json
                        break
                    except:
                        continue
        except Exception as e:
            if not error_msg:  # Only update if we don't have an error message yet
                error_msg = f"Error extracting JSON with brace pattern: {str(e)}"
    
    # Third attempt: Try to parse the entire response as JSON
    if not json_str:
        try:
            parsed_json = json.loads(response_text.strip())
            json_str = response_text.strip()
        except Exception as e:
            if not error_msg:
                error_msg = f"Could not find valid JSON in response: {str(e)}"
    
    # If we have a JSON string, try to extract scores and justifications
    scores_dict = {}
    justifications_dict = {}
    
    if json_str:
        try:
            review_data = json.loads(json_str)
            
            # Extract scores: Pattern is "p<number>_score" or "P<number>_score" or "P<number>" or "p<number>"
            for key in review_data:
                lowercase_key = key.lower()
                
                # Handle score fields
                if lowercase_key.startswith('p') and ('score' in lowercase_key or lowercase_key.replace('p', '').isdigit()):
                    # Extract the number part (e.g., extract '1' from 'p1_score')
                    if '_score' in lowercase_key:
                        p_num = lowercase_key.split('_')[0].replace('p', '')
                    else:
                        p_num = lowercase_key.replace('p', '')
                        
                    if p_num.isdigit() or p_num == 'overall':
                        # Format the key consistently as 'P1', 'P2', etc. or 'Overall'
                        score_key = f"P{p_num}" if p_num.isdigit() else 'Overall'
                        scores_dict[score_key] = review_data[key]
                
                # Handle justification fields
                elif lowercase_key.startswith('p') and 'justification' in lowercase_key:
                    # Extract the number part (e.g., extract '1' from 'p1_justification')
                    p_num = lowercase_key.split('_')[0].replace('p', '')
                    
                    if p_num.isdigit() or p_num == 'overall':
                        # Format the key consistently
                        justification_key = f"P{p_num}" if p_num.isdigit() else 'Overall'
                        justifications_dict[justification_key] = review_data[key]
                        
                # Handle overall score and justification specifically (sometimes they're named differently)
                elif lowercase_key == 'overall_score':
                    scores_dict['Overall'] = review_data[key]
                elif lowercase_key == 'overall_justification':
                    justifications_dict['Overall'] = review_data[key]
            
            # If we found some data but error_msg still exists, we'll include it as a warning but continue
            if scores_dict and error_msg:
                error_msg = f"Warning: {error_msg} but managed to extract some data"
            elif not scores_dict and not error_msg:
                error_msg = "Could not extract any scores from the response"
                
        except Exception as e:
            error_msg = f"Error parsing extracted JSON: {str(e)}"
            logger.error(f"Error parsing JSON for {context}: {str(e)}")
            logger.debug(f"Problematic JSON string: {json_str[:500]}...")
    
    return scores_dict, justifications_dict, error_msg