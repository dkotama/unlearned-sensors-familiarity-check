#!/usr/bin/env python3
"""
Main entry point for the LLM Sensor Knowledge Comparison application.
This CLI tool allows users to compare responses from different LLMs about sensor datasheets.
"""

import os
import time
import click
import sys
import json
import glob
import logging
import yaml
import pandas as pd
from datetime import datetime
import re

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TextColumn, SpinnerColumn
from rich.spinner import Spinner

# Import our new utils module with the improved JSON parser
from src.utils import extract_json_from_llm_response

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Other imports
try:
    import numpy as np
    logger.info(f"NumPy version: {np.__version__}")
except ImportError as e:
    logger.error(f"NumPy import error: {e}")
# Add the parent directory to sys.path to import other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api_client import APIClientFactory
from src.prompt_generator import PromptGenerator
from src.result_processor import ResultProcessor
from src.metrics_logger import MetricsLogger
from src.datasheet_loader import OfficialDatasheetLoader
from src.review_logger import ReviewScoreLogger

console = Console()

def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def display_sensors(df):
    """Display available sensors in a table, including an 'All Sensors' option."""
    table = Table(title="Available Sensors")
    table.add_column("Index", style="cyan")
    table.add_column("Brand", style="magenta")
    table.add_column("Type", style="green")
    
    # Add "All Sensors" option
    table.add_row("0", "All Sensors", "")
    
    for idx, row in df.iterrows():
        # Adjust index to be 1-based for display
        table.add_row(str(idx + 1), row['Brand'], row['Type'])
    
    console.print(table)

def display_models(models):
    """Display available models in a table, including an 'All Models' option."""
    table = Table(title="Available Models")
    table.add_column("Index", style="cyan")
    table.add_column("Model ID", style="magenta")
    table.add_column("Provider", style="green")

    # Add "All Models" option
    table.add_row("0", "All Models", "")

    for idx, model in enumerate(models):
        # Adjust index to be 1-based for display
        table.add_row(str(idx + 1), model['id'], model['provider'])

    console.print(table)

def display_reviewer_models(models, console_instance):
    """Display available reviewer models in a table."""
    table = Table(title="Available Reviewer Models")
    table.add_column("Index", style="cyan")
    table.add_column("Model ID", style="magenta")
    table.add_column("Provider", style="green")

    if not models:
        console_instance.print("[yellow]No reviewer models configured.[/yellow]")
        return False # Indicate no models to select

    for idx, model in enumerate(models):
        # Adjust index to be 1-based for display
        table.add_row(str(idx + 1), model['id'], model['provider'])
    
    console_instance.print(table)
    return True # Indicate models were displayed

def create_api_client(model_id: str, cfg: dict, purpose: str = "generator"):
    """
    Finds model configuration and creates an API client.
    Searches appropriate model lists based on purpose.

    Args:
        model_id (str): The ID of the model to find.
        cfg (dict): The application configuration dictionary.
        purpose (str): The purpose of the model ("generator" or "reviewer").

    Returns:
        APIClient: An instance of the API client for the found model.

    Raises:
        ValueError: If the model_id is not found, provider configuration is missing/invalid,
                    or an invalid purpose is specified.
    """
    model_config = None
    searched_lists_description = "" # For error messages

    if purpose == "reviewer":
        primary_list_name = 'reviewer_models'
        fallback_list_name = 'models'
        searched_lists_description = f"'{primary_list_name}' and (if not found there) '{fallback_list_name}'"

        primary_list = cfg.get(primary_list_name, [])
        for m_cfg in primary_list:
            if m_cfg.get('id') == model_id:
                model_config = m_cfg
                break
        
        if not model_config:
            fallback_list = cfg.get(fallback_list_name, [])
            for m_cfg in fallback_list:
                if m_cfg.get('id') == model_id:
                    model_config = m_cfg
                    break
    elif purpose == "generator":
        primary_list_name = 'models'
        searched_lists_description = f"'{primary_list_name}'"
        primary_list = cfg.get(primary_list_name, [])
        for m_cfg in primary_list:
            if m_cfg.get('id') == model_id:
                model_config = m_cfg
                break
    else:
        raise ValueError(f"Invalid purpose '{purpose}'. Must be 'generator' or 'reviewer'.")

    if not model_config:
        raise ValueError(f"Model ID '{model_id}' not found in the {searched_lists_description} list(s) in your configuration.")

    provider_name = model_config.get('provider')
    if not provider_name:
        raise ValueError(f"Provider not specified for model ID '{model_id}' in its configuration (found in {searched_lists_description} list(s)).")

    actual_provider_config = cfg.get('providers', {}).get(provider_name)
    if not actual_provider_config:
        raise ValueError(f"Configuration for provider '{provider_name}' (required by model '{model_id}') not found in 'providers' section of your config.")

    if 'api_key' not in actual_provider_config or not actual_provider_config['api_key']:
        raise ValueError(f"API key for provider '{provider_name}' (required by model '{model_id}') is missing or empty. Please check 'providers.{provider_name}.api_key' in your config.")

    # APIClientFactory is imported at the top of src/main.py
    return APIClientFactory.get_client(actual_provider_config, provider_name)
@click.group()
def cli():
    """LLM Sensor Knowledge Comparison Tool"""
    pass

@cli.command()
@click.option('--config', default='config/config.yaml', help='Path to configuration file')
@click.option('--convert-pdf', is_flag=True, help='Convert the last generated output to PDF after comparison')
def run(config, convert_pdf):
    """Run the comparison tool with interactive selection."""
    # Load configuration
    cfg = load_config(config)
    
    # Initialize components
    prompt_gen = PromptGenerator(cfg['prompt_template_path'])
    result_proc = ResultProcessor(cfg['results_base_path'])
    metrics_logger = MetricsLogger(cfg['metrics_log_path'])
    
    # Create API clients for each provider
    clients = {}
    for provider_name, provider_config in cfg['providers'].items():
        clients[provider_name] = APIClientFactory.get_client(provider_config, provider_name)
    
    # Load sensor data
    sensors_df = pd.read_csv(cfg['data_path'])
    
    console.print("[bold green]Welcome to LLM Sensor Knowledge Comparison Tool[/bold green]")
    console.print("")
    
    # Display and select sensors
    display_sensors(sensors_df)
    sensor_indices = click.prompt("Select sensor indices (comma-separated, or 'all')", default="all")
    if sensor_indices.lower() == 'all':
        selected_sensors = sensors_df
    else:
        indices = [int(i.strip()) for i in sensor_indices.split(',')]
        selected_sensors = sensors_df.iloc[indices]
    
    # Display and select models
    display_models(cfg['models'])
    model_indices = click.prompt("Select model indices (comma-separated, or 'all')", default="all")
    if model_indices.lower() == 'all':
        selected_models = cfg['models']
    else:
        indices = [int(i.strip()) for i in model_indices.split(',')]
        selected_models = [cfg['models'][i] for i in indices]
    
    console.print(f"[bold]Selected Sensors:[/bold] {len(selected_sensors)}")
    console.print(f"[bold]Selected Models:[/bold] {len(selected_models)}")
    if not click.confirm("Proceed with comparison?"):
        console.print("[bold red]Aborted.[/bold red]")
        return
    
    # Process each sensor with each model
    total_requests = len(selected_sensors) * len(selected_models)
    console.print(f"[bold blue]Processing {total_requests} requests...[/bold blue]")
    
    with console.status("[bold green]Working on requests...[/bold green]") as status:
        completed = 0
        for _, sensor in selected_sensors.iterrows():
            sensor_brand = sensor['Brand']
            sensor_type = sensor['Type']
            # Generate prompt for this sensor (no datasheet content needed as per updated requirements)
            prompt = prompt_gen.generate_prompt(sensor_brand, sensor_type, "")
            
            for model_info in selected_models:
                model_id = model_info['id']
                provider = model_info['provider']
                completed += 1
                status.update(f"[bold green]Processing request {completed}/{total_requests}: {sensor_brand} {sensor_type} with {model_id} via {provider}[/bold green]")
                
                # Select the appropriate client based on provider
                client = clients.get(provider)
                if not client:
                    console.print(f"[red]✗ Error on {completed}/{total_requests}: No client found for provider {provider}[/red]")
                    continue
                
                # Send request to model
                start_time = datetime.now()
                try:
                    response = client.send_request(model_id, prompt)
                    end_time = datetime.now()
                    
                    response_time = (end_time - start_time).total_seconds()
                    input_tokens = response.get('input_tokens', 0)
                    output_tokens = response.get('output_tokens', 0)
                    response_text = response.get('text', '')
                    response_length = len(response_text)
                    
                    # Save result
                    result_filename = result_proc.save_result(sensor_brand, sensor_type, model_id, response_text)
                    
                    # Log metrics
                    metrics_logger.log_metrics(
                        sensor_brand, sensor_type, model_id,
                        response_time, input_tokens, output_tokens, response_length
                    )
                    
                    console.print(f"[green]✓ Completed {completed}/{total_requests}: {sensor_brand} {sensor_type} with {model_id} (saved to {result_filename})[/green]")
                except Exception as e:
                    error_msg = f"Error on {completed}/{total_requests}: {sensor_brand} {sensor_type} with {model_id}: {str(e)}"
                    console.print(f"[red]✗ {error_msg}[/red]")
                    # Log detailed error with traceback to file
                    import traceback
                    detailed_error = f"API Error on {completed}/{total_requests}: {sensor_brand} {sensor_type} with {model_id}\n{traceback.format_exc()}"
                    log_error(detailed_error, cfg.get('logs_path', 'logs/'))

            # Check if there are more sensors to process and apply delay if configured
            # Log types and values for debugging
            console.print(f"[debug]sensor.index type: {type(sensor.index)}, value: {sensor.index}")
            console.print(f"[debug]selected_sensors.index[-1] type: {type(selected_sensors.index[-1])}, value: {selected_sensors.index[-1]}")
            try:
                # Check if this is not the last sensor by comparing indices
                is_not_last = sensor.name != selected_sensors.index[-1]
                if is_not_last:  # If this is not the last sensor
                    delay_seconds = cfg.get('sensor_delay_seconds', 0)
                    if delay_seconds > 0:
                        console.print(f"[bold yellow]Waiting {delay_seconds} seconds before processing the next sensor...[/bold yellow]")
                        for remaining in range(delay_seconds, 0, -1):
                            console.print(f"[yellow]Countdown: {remaining} seconds remaining...[/yellow]", end='\r')
                            import time
                            time.sleep(1)
                        console.print("")  # New line after countdown
            except Exception as e:
                console.print(f"[red]Error in sensor index comparison: {str(e)}[/red]")
                log_error(f"Index comparison error: {str(e)}", cfg['logs_path'])
                # Failsafe: Assume it's not the last sensor to continue processing
                is_not_last = True
    
    console.print("[bold green]All requests completed![/bold green]")
    
    # Start PDF conversion process for generated .md files
    logger.info("PDF conversion is about to start for all files.")
    console.print("[bold blue]Starting PDF conversion of .md files using pandoc...[/bold blue]")
    if convert_pdf:
        convert_to_pdf(cfg, convert_last_only=True)

@cli.command()
@click.option('--config', default='config/config.yaml', help='Path to configuration file')
def convert_pdf(config):
    """Convert existing .md files in results directory to PDF."""
    cfg = load_config(config)
    console.print("[bold blue]Starting manual PDF conversion of .md files...[/bold blue]")
    convert_to_pdf(cfg)

def convert_to_pdf(cfg, convert_last_only=False):
    """Convert .md files to PDF using pandoc."""
    import subprocess
    import glob
    
    results_path = cfg['results_base_path']
    pdf_base_path = os.path.join(os.path.dirname(results_path), 'pdf')
    
    # Ensure the base pdf directory exists
    os.makedirs(pdf_base_path, exist_ok=True)
    
    # Find all .md files in results directory and subdirectories
    logger.info(f"Searching for .md files in {results_path}")
    if convert_last_only:
        all_md_files = glob.glob(os.path.join(results_path, '**', '*.md'), recursive=True)
        if all_md_files:
            latest_file = max(all_md_files, key=os.path.getmtime)
            md_files = [latest_file]
        else:
            md_files = []
    else:
        md_files = glob.glob(os.path.join(results_path, '**', '*.md'), recursive=True)
    total_files = len(md_files)
    converted = 0
    
    if total_files == 0:
        console.print("[yellow]No .md files found to convert.[/yellow]")
    else:
        console.print(f"[bold blue]Found {total_files} .md files to convert to PDF.[/bold blue]")
        with console.status("[bold green]Converting files to PDF...[/bold green]") as status:
            for md_file in md_files:
                converted += 1
                # Calculate relative path to maintain subfolder structure
                relative_path = os.path.relpath(md_file, results_path)
                pdf_dir = os.path.dirname(os.path.join(pdf_base_path, relative_path))
                pdf_file = os.path.splitext(os.path.basename(md_file))[0] + '.pdf'
                pdf_path = os.path.join(pdf_dir, pdf_file)
                
                # Create corresponding pdf subdirectory if it doesn't exist
                os.makedirs(pdf_dir, exist_ok=True)
                
                status.update(f"[bold green]Converting file {converted}/{total_files}: {relative_path}[/bold green]")
                try:
                    # Run pandoc command to convert .md to PDF with XeLaTeX to handle Unicode characters
                    # Add filename in the footer using LaTeX formatting
                    footer_command = "\\usepackage{fancyhdr}\\pagestyle{fancy}\\fancyfoot[C]{" + os.path.basename(md_file).replace("_", "\\_") + "}"
                    subprocess.run(['pandoc', md_file, '-o', pdf_path, '--pdf-engine=xelatex', '-V', f"header-includes={footer_command}"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    console.print(f"[green]✓ Converted {converted}/{total_files}: {relative_path} to PDF (saved to {pdf_path})[/green]")
                except subprocess.CalledProcessError as e:
                    console.print(f"[red]✗ Error converting {converted}/{total_files}: {relative_path} to PDF: {str(e.stderr.decode())}[/red]")
                except FileNotFoundError:
                    console.print(f"[red]✗ Error: 'pandoc' not found. Please ensure pandoc is installed on your system.[/red]")
                    console.print(f"[red]Visit https://pandoc.org/installing.html for installation instructions.[/red]")
                    break
                except Exception as e:
                    console.print(f"[red]✗ Unexpected error converting {converted}/{total_files}: {relative_path} to PDF: {str(e)}[/red]")
    
    console.print("[bold green]PDF conversion process completed![/bold green]")
    # The function is already defined and called with cfg, no need to reload config or duplicate code

def log_error(error_msg, logs_path):
    """Log error message to a file in the specified logs directory."""
    os.makedirs(logs_path, exist_ok=True)
    log_file = os.path.join(logs_path, f"error_log_{datetime.now().strftime('%Y%m%d')}.txt")
    with open(log_file, 'a') as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {error_msg}\n")

@cli.command()
@click.option('--config', default='config/config.yaml', help='Path to configuration file')
@click.option('--reviewer', help="Specific reviewer model. If omitted, you'll be prompted to select from a list (defaults to config setting).")
@click.option('--sensor', help="Sensor to review (Brand_Type format). If omitted, you'll be prompted to select from a list (supports 'all').")
def review(config, reviewer, sensor):
    """Review and score generated datasheets against official ones.
    This command reviews all found generated datasheets for a given sensor.
    """
    # Load configuration
    cfg = load_config(config)
    # Load sensor data for selection
    sensors_df = pd.read_csv(cfg['data_path'])

    if sensor is None:
        console.print("[bold blue]Select a sensor to review:[/bold blue]")
        display_sensors(sensors_df)
        
        while True:
            try:
                sensor_choice_str = click.prompt("Enter the number for the sensor (0 for All Sensors)", type=str)
                sensor_choice = int(sensor_choice_str)
                
                if sensor_choice == 0:
                    sensor = "ALL_SENSORS" # Special value for all sensors
                    console.print(f"Selected: [bold cyan]All Sensors[/bold cyan]")
                    break
                # Adjust for 1-based indexing for specific sensors (user inputs 1, df index is 0)
                elif 1 <= sensor_choice <= len(sensors_df):
                    # Convert 1-based input to 0-based DataFrame index
                    selected_sensor_row = sensors_df.iloc[sensor_choice - 1]
                    sensor = f"{selected_sensor_row['Brand']}_{selected_sensor_row['Type']}"
                    console.print(f"Selected sensor: [bold cyan]{sensor}[/bold cyan]")
                    break
                else:
                    console.print(f"[bold red]Invalid selection. Please enter a valid number from the list.[/bold red]")
            except ValueError:
                console.print("[bold red]Invalid input. Please enter a number.[/bold red]")
            except IndexError: # Should not happen with iloc if length check is correct
                 console.print(f"[bold red]Invalid index. Please enter a valid number from the list.[/bold red]")
            except Exception as e:
                console.print(f"[bold red]An error occurred during sensor selection: {e}. Please try again.[/bold red]")
    else:
        # If sensor is provided via CLI, use it directly.
        console.print(f"Using sensor from CLI: [bold cyan]{sensor}[/bold cyan]")

    # Reviewer model selection
    # Generator model selection is removed; all found datasheets for a sensor will be processed.
    if reviewer is None:  # If --reviewer CLI option was not used
        console.print("\n[bold blue]Select a reviewer model:[/bold blue]")
        # Assuming reviewer models are listed in the main 'models' section of the config
        available_reviewer_models = cfg.get('reviewer_models', cfg.get('models', []))
        
        if display_reviewer_models(available_reviewer_models, console):
            while True:
                try:
                    reviewer_choice_str = click.prompt(
                        "Enter the number for the reviewer model (or press Enter to use default/config setting)",
                        default="", show_default=False, type=str
                    )
                    if not reviewer_choice_str:  # User pressed Enter
                        console.print("[italic]No reviewer selected interactively, will use default/config setting if available.[/italic]")
                        # 'reviewer' remains None, will be handled by subsequent logic
                        break
                    
                    reviewer_choice = int(reviewer_choice_str)
                    
                    # Adjust for 1-based indexing
                    if 1 <= reviewer_choice <= len(available_reviewer_models):
                        selected_reviewer_info = available_reviewer_models[reviewer_choice - 1]
                        reviewer = selected_reviewer_info['id']  # Update 'reviewer' variable
                        console.print(f"Selected reviewer model: [bold cyan]{reviewer}[/bold cyan]")
                        break
                    else:
                        console.print(f"[bold red]Invalid selection. Please enter a valid number from the list.[/bold red]")
                except ValueError:
                    console.print("[bold red]Invalid input. Please enter a number or press Enter.[/bold red]")
                except Exception as e:
                    console.print(f"[bold red]An error occurred during reviewer model selection: {e}. Please try again.[/bold red]")
        else:
            # display_reviewer_models printed "No reviewer models configured." or similar
            console.print("[yellow]No reviewer models available for interactive selection. Will use default/config if set.[/yellow]")
            # 'reviewer' remains None
    else:
        console.print(f"Using reviewer model from CLI: [bold cyan]{reviewer}[/bold cyan]")

    # Initialize components
    datasheet_loader = OfficialDatasheetLoader(cfg['data_path'])
    review_logger = ReviewScoreLogger(cfg['reviews_base_path'])
    
    # Determine the final reviewer model ID and get its configuration
    final_reviewer_model_id = reviewer  # This is from CLI, interactive selection, or still None
    if final_reviewer_model_id is None:
        final_reviewer_model_id = cfg.get('default_reviewer_model') # Fallback to default from config

    if not final_reviewer_model_id:
        console.print("[red]No reviewer model specified, selected, or found in config as default. Cannot proceed with review.[/red]")
        return
    
    try:
        reviewer_client = create_api_client(final_reviewer_model_id, cfg, purpose="reviewer")
        
        # The create_api_client function has already found and validated the model.
        # We need reviewer_config primarily for the print statement that follows.
        # We'll retrieve it using the same logic as create_api_client for 'reviewer' purpose.
        _model_conf = None
        _primary_list = cfg.get('reviewer_models', [])
        for m_cfg_iter in _primary_list:
            if m_cfg_iter.get('id') == final_reviewer_model_id:
                _model_conf = m_cfg_iter
                break
        if not _model_conf:
            _fallback_list = cfg.get('models', [])
            for m_cfg_iter in _fallback_list:
                if m_cfg_iter.get('id') == final_reviewer_model_id:
                    _model_conf = m_cfg_iter
                    break
        
        reviewer_config = _model_conf
        if not reviewer_config:
            console.print(f"[yellow]Warning: Could not re-fetch reviewer_config for '{final_reviewer_model_id}' for printing, though client creation succeeded.[/yellow]")
            reviewer_config = {'provider': 'unknown'} # Fallback for print

    except ValueError as e:
        console.print(f"[red]Failed to initialize reviewer API client for '{final_reviewer_model_id}': {e}[/red]")
        return
    except Exception as e:
        console.print(f"[red]An unexpected error occurred while creating API client for reviewer '{final_reviewer_model_id}': {e}[/red]")
        return
        
    console.print(f"Using reviewer: [bold magenta]{final_reviewer_model_id}[/bold magenta] via provider [bold green]{reviewer_config['provider']}[/bold green]")
    # Process reviews
    logger.info("Starting review process...")

    # 1. Initialization (continued)
    # Note: datasheet_loader and review_logger were initialized earlier (lines 496-497)
    # We need to ensure they use the correct paths as per spec if different from initial config.
    # The spec implies 'datasheet_path' and 'review_results_path' from cfg, or hardcoded defaults.
    
    official_datasheet_root_path = cfg.get('datasheet_path', 'datasheet/')
    # Re-initialize or update path if necessary. Assuming OfficialDatasheetLoader can be re-init or path updated.
    # For simplicity, let's assume re-initialization is fine.
    datasheet_loader = OfficialDatasheetLoader(official_datasheet_root_path)
    logger.info(f"OfficialDatasheetLoader re-initialized with specific path: {official_datasheet_root_path}")

    review_results_base_path = cfg.get('review_results_path', 'results/reviews/')
    review_logger = ReviewScoreLogger(review_results_base_path) # Re-initialize
    logger.info(f"ReviewScoreLogger re-initialized with specific path: {review_results_base_path}")

    try:
        with open("prompts/review_criteria_prompt.txt", 'r', encoding='utf-8') as f:
            review_prompt_template = f.read()
        logger.info("Successfully loaded review_criteria_prompt.txt")
    except FileNotFoundError:
        logger.error("prompts/review_criteria_prompt.txt not found.")
        console.print("[bold red]Error: prompts/review_criteria_prompt.txt not found. Aborting review.[/bold red]")
        return
    except Exception as e:
        logger.error(f"Error loading prompts/review_criteria_prompt.txt: {e}", exc_info=True)
        console.print(f"[bold red]Error loading review prompt: {e}. Aborting review.[/bold red]")
        return

    # 2. Determine Sensors to Process
    # sensors_df is loaded at the beginning of the review function (line 388)
    sensors_to_process_list = []
    if sensor == "ALL_SENSORS":
        if sensors_df is not None and not sensors_df.empty:
            for _, row_data in sensors_df.iterrows():
                sensors_to_process_list.append({'brand': row_data['Brand'], 'type': row_data['Type']})
            logger.info(f"Processing all {len(sensors_to_process_list)} sensors from sensors.csv.")
        else:
            logger.warning("ALL_SENSORS selected, but no sensor data loaded (sensors_df is empty or None).")
            console.print("[yellow]Warning: ALL_SENSORS selected, but no sensor data found in sensors.csv.[/yellow]")
    else:
        # Specific sensor 'Brand_Type'
        try:
            brand_val, sensor_type_val = sensor.split('_', 1)
            sensors_to_process_list.append({'brand': brand_val, 'type': sensor_type_val})
            logger.info(f"Processing selected sensor: Brand={brand_val}, Type={sensor_type_val}")
        except ValueError:
            logger.error(f"Invalid sensor format: {sensor}. Expected Brand_Type.")
            console.print(f"[bold red]Error: Invalid sensor format '{sensor}'. Expected Brand_Type. Aborting review.[/bold red]")
            return
    
    if not sensors_to_process_list:
        console.print("[yellow]No sensors to process. Exiting review.[/yellow]")
        logger.info("No sensors to process. Exiting review.")
        return

    # 3. Iterate Through Sensors
    for sensor_info_item in sensors_to_process_list:
        current_brand = sensor_info_item['brand']
        current_sensor_type = sensor_info_item['type']
        logger.info(f"Reviewing sensor: {current_brand}_{current_sensor_type}")
        console.print(f"\n[bold blue]Reviewing Sensor: {current_brand} {current_sensor_type}[/bold blue]")

        official_datasheet_content = None
        official_datasheet_status = "Not Loaded"
        try:
            # datasheet_loader was initialized with official_datasheet_root_path
            official_datasheet_content, official_datasheet_status = datasheet_loader.load_datasheet(current_brand, current_sensor_type)
            if official_datasheet_content is None:
                logger.warning(f"Official datasheet not found or failed to load for {current_brand}_{current_sensor_type}. Status: {official_datasheet_status}")
                console.print(f"  [yellow]Warning: Official datasheet for {current_brand}_{current_sensor_type} not loaded. Status: {official_datasheet_status}. Reviews will note this.[/yellow]")
            else:
                logger.info(f"Successfully loaded official datasheet for {current_brand}_{current_sensor_type}. Length: {len(official_datasheet_content)} chars. Status: {official_datasheet_status}")
        except Exception as e:
            logger.error(f"Error loading official datasheet for {current_brand}_{current_sensor_type}: {e}", exc_info=True)
            console.print(f"  [red]Error loading official datasheet for {current_brand}_{current_sensor_type}: {e}. Reviews will note this.[/red]")
            official_datasheet_status = f"Error loading: {str(e)}"
        
        # 4. Find and Iterate Through Generated Datasheets for the Current Sensor
        sensor_directory_name = f"{current_brand}_{current_sensor_type}"
        generated_datasheets_dir = os.path.join(cfg.get('results_base_path', 'results/'), sensor_directory_name)
        search_pattern = os.path.join(generated_datasheets_dir, '*.md')
        logger.info(f"Searching for generated datasheets in: {generated_datasheets_dir} with pattern: *.md")
        found_generated_datasheets_paths = glob.glob(search_pattern)

        if not found_generated_datasheets_paths:
            logger.warning(f"No generated datasheets found in {generated_datasheets_dir} for sensor {current_brand}_{current_sensor_type}")
            console.print(f"  [yellow]No generated datasheets found in {generated_datasheets_dir}. Skipping review for this sensor.[/yellow]")
            continue # To the next sensor_info_item

        for gen_ds_path in found_generated_datasheets_paths:
            filename = os.path.basename(gen_ds_path)
            logger.info(f"Reviewing generated datasheet: {gen_ds_path}")
            console.print(f"    [cyan]File: {filename}[/cyan]")

            # Parse filename to extract GeneratorProvider and GeneratorModelName
            # Filename convention: [GeneratorProvider]_[GeneratorModelName]_[Timestamp...].md
            filename_stem = filename[:-3] # Remove .md extension
            parts = filename_stem.split('_')

            if len(parts) < 2: # Need at least Provider_Model
                logger.warning(f"Filename '{filename}' does not conform to 'Provider_Model[_Timestamp...].md' pattern. Skipping.")
                console.print(f"      [yellow]Could not parse provider and model from filename '{filename}'. Skipping.[/yellow]")
                continue # To the next gen_ds_path

            generated_model_provider = parts[0]
            # Assuming model name is the second part, as per example "openrouter_claude-3.5-haiku_..."
            generated_model_name_simple = parts[1]

            logger.info(f"Parsed from filename '{filename}': Provider='{generated_model_provider}', ModelName='{generated_model_name_simple}'")
            console.print(f"    [bold magenta]Generator: {generated_model_provider} - {generated_model_name_simple}[/bold magenta]")
            
            generated_datasheet_content = ""
            try:
                with open(gen_ds_path, 'r', encoding='utf-8') as f_gen:
                    generated_datasheet_content = f_gen.read()
                logger.info(f"Successfully read generated datasheet: {gen_ds_path}")
            except Exception as e:
                logger.error(f"Error reading generated datasheet {gen_ds_path}: {e}", exc_info=True)
                console.print(f"      [red]Error reading file {filename}: {e}. Skipping.[/red]")
                continue # Next gen_ds_path
            
            # Prepare base log data, common for all outcomes for this file
            log_data_base = {
                "Sensor_Brand": current_brand, "Sensor_Type": current_sensor_type,
                "Generated_Datasheet_LLM_Provider": generated_model_provider, # Parsed from filename
                "Generated_Datasheet_LLM_Model": generated_model_name_simple,    # Parsed from filename
                "Generated_Datasheet_Filename": filename,
                "Official_Datasheet_Status": official_datasheet_status,
                "Review_Timestamp": datetime.now().isoformat(),
            }
            # Reviewer LLM Provider and Model (final_reviewer_model_id is set)
            reviewer_llm_provider_name_val = "N/A"
            reviewer_llm_model_name_simple_val = final_reviewer_model_id # Fallback
            if reviewer_config and reviewer_config.get('provider') != 'unknown':
                reviewer_llm_provider_name_val = reviewer_config['provider']
                if final_reviewer_model_id.startswith(reviewer_llm_provider_name_val + '_'):
                     reviewer_llm_model_name_simple_val = final_reviewer_model_id[len(reviewer_llm_provider_name_val)+1:]
            
            log_data_base["Reviewer_LLM_Provider"] = reviewer_llm_provider_name_val
            log_data_base["Reviewer_LLM_Model"] = reviewer_llm_model_name_simple_val

            if official_datasheet_content is None:
                logger.warning(f"Skipping LLM review for {gen_ds_path} as official datasheet content is missing.")
                console.print(f"      [yellow]Skipping LLM review as official datasheet content is missing. Logging status.[/yellow]")
                log_data_missing_official = {**log_data_base}
                for i in range(1, 17): # P1-P16
                    log_data_missing_official[f'P{i}_Score'] = "N/A"
                    log_data_missing_official[f'P{i}_Justification'] = "Official datasheet content was not available for comparison."
                log_data_missing_official["Overall_Score"] = "N/A"
                log_data_missing_official["Overall_Justification"] = "Official datasheet content was not available for comparison."
                log_data_missing_official["Average_Pn_Score"] = "N/A"
                try:
                    scores_dict = {}
                    just_dict = {}
                    for i in range(1, 17):
                        scores_dict[f'P{i}'] = "N/A"
                        just_dict[f'P{i}'] = "Official datasheet content was not available for comparison."
                    scores_dict['Overall'] = "N/A"
                    just_dict['Overall'] = "Official datasheet content was not available for comparison."

                    review_logger.log_review(
                        reviewer_provider=log_data_missing_official['Reviewer_LLM_Provider'],
                        reviewer_model=log_data_missing_official['Reviewer_LLM_Model'],
                        sensor_brand=log_data_missing_official['Sensor_Brand'],
                        sensor_type=log_data_missing_official['Sensor_Type'],
                        generator_provider=log_data_missing_official['Generated_Datasheet_LLM_Provider'],
                        generator_model=log_data_missing_official['Generated_Datasheet_LLM_Model'],
                        official_datasheet_status=log_data_missing_official['Official_Datasheet_Status'],
                        scores=scores_dict,
                        justifications=just_dict
                    )
                except Exception as log_e:
                    logger.error(f"Failed to log missing official datasheet info for {gen_ds_path}: {log_e}", exc_info=True)
                continue # Next gen_ds_path

            full_review_prompt = review_prompt_template.replace("{{OFFICIAL_DATASHEET_CONTENT}}", official_datasheet_content)
            full_review_prompt = full_review_prompt.replace("{{GENERATED_DATASHEET_CONTENT}}", generated_datasheet_content)

            review_response_json_str = None
            review_response_data = {}
            try:
                logger.info(f"Sending review request to {final_reviewer_model_id} for {gen_ds_path}. Prompt length: {len(full_review_prompt)}")
                
                # Add retry mechanism for API calls
                max_retries = 3
                retry_delay = 5  # seconds
                last_error = None
                
                for retry_attempt in range(max_retries):
                    try:
                        if retry_attempt > 0:
                            logger.info(f"Retry attempt {retry_attempt}/{max_retries} for {gen_ds_path}")
                            console.print(f"      [yellow]Retry attempt {retry_attempt}/{max_retries}...[/yellow]")
                            time.sleep(retry_delay * retry_attempt)  # Exponential backoff
                            
                        api_response = reviewer_client.send_request(model=final_reviewer_model_id, prompt=full_review_prompt)
                        
                        if isinstance(api_response, dict) and 'text' in api_response:
                            review_response_json_str = api_response['text']
                        elif isinstance(api_response, str):
                            review_response_json_str = api_response
                        else:
                            logger.warning(f"Unexpected response type from reviewer LLM: {type(api_response)}. Attempting to stringify.")
                            review_response_json_str = str(api_response)
                        
                        logger.info(f"Received review from {final_reviewer_model_id} for {gen_ds_path}. Response length: {len(review_response_json_str if review_response_json_str else '')}")
                        
                        # Break out of retry loop on success
                        break
                        
                    except Exception as retry_e:
                        last_error = retry_e
                        logger.warning(f"API call attempt {retry_attempt+1}/{max_retries} failed: {str(retry_e)}")
                        if retry_attempt == max_retries - 1:
                            # Re-raise the exception on the last retry attempt
                            raise last_error
                
            except Exception as e:
                logger.error(f"Error calling reviewer LLM for {gen_ds_path}: {e}", exc_info=True)
                console.print(f"      [red]Error calling reviewer LLM: {e}. Skipping this file.[/red]")
                log_data_failed_review = {**log_data_base}
                for i in range(1, 17): log_data_failed_review[f'P{i}_Score'] = "LLM_Error"; log_data_failed_review[f'P{i}_Justification'] = f"LLM API Error: {str(e)[:250]}"
                log_data_failed_review["Overall_Score"] = "LLM_Error"; log_data_failed_review["Overall_Justification"] = f"LLM API Error: {str(e)[:250]}"
                log_data_failed_review["Average_Pn_Score"] = "LLM_Error"
                try:
                    scores_dict = {}
                    just_dict = {}
                    for i in range(1, 17):
                        scores_dict[f'P{i}'] = "LLM_Error"
                        just_dict[f'P{i}'] = f"LLM API Error: {str(e)[:250]}"
                    scores_dict['Overall'] = "LLM_Error"
                    just_dict['Overall'] = f"LLM API Error: {str(e)[:250]}"

                    review_logger.log_review(
                        reviewer_provider=log_data_failed_review.get('Reviewer_LLM_Provider'),
                        reviewer_model=log_data_failed_review.get('Reviewer_LLM_Model'),
                        sensor_brand=log_data_failed_review.get('Sensor_Brand'),
                        sensor_type=log_data_failed_review.get('Sensor_Type'),
                        generator_provider=log_data_failed_review.get('Generated_Datasheet_LLM_Provider'),
                        generator_model=log_data_failed_review.get('Generated_Datasheet_LLM_Model'),
                        official_datasheet_status=log_data_failed_review.get('Official_Datasheet_Status', 'Error during review'),
                        scores={},
                        justifications={}
                    )
                except Exception as log_e: logger.error(f"Failed to log API error info for {gen_ds_path}: {log_e}", exc_info=True)
                continue # Next gen_ds_path
            
            if review_response_json_str:
                try:
                    # Use our new robust JSON parser instead of manual JSON parsing
                    sensor_info = f"{current_brand}_{current_sensor_type}"
                    model_info = f"{generated_model_provider}_{generated_model_name_simple}"
                    
                    scores_dict, justifications_dict, error_msg = extract_json_from_llm_response(
                        review_response_json_str, 
                        sensor_info=sensor_info,
                        model_info=model_info
                    )
                    
                    if error_msg:
                        logger.warning(f"Warning while parsing review for {gen_ds_path}: {error_msg}")
                        console.print(f"      [yellow]Warning while parsing review: {error_msg}[/yellow]")
                    
                    # Handle API errors gracefully
                    if not scores_dict and error_msg and error_msg.startswith("API error:"):
                        logger.error(f"API error for {gen_ds_path}: {error_msg}")
                        console.print(f"      [red]API error detected: {error_msg}. Logging with N/A values.[/red]")
                        
                        # Create empty scores with 'API_Error' as values
                        scores_dict = {}
                        justifications_dict = {}
                        for i in range(1, 17):
                            scores_dict[f'P{i}'] = "API_Error"
                            justifications_dict[f'P{i}'] = f"API Error: {error_msg}"
                        scores_dict['Overall'] = "API_Error"
                        justifications_dict['Overall'] = f"API Error: {error_msg}"
                        
                        # Still log the review with error indicators
                        review_logger.log_review(
                            reviewer_provider=reviewer_llm_provider_name_val,
                            reviewer_model=reviewer_llm_model_name_simple_val,
                            sensor_brand=current_brand,
                            sensor_type=current_sensor_type,
                            generator_provider=generated_model_provider,
                            generator_model=generated_model_name_simple,
                            official_datasheet_status=official_datasheet_status,
                            scores=scores_dict,
                            justifications=justifications_dict
                        )
                        console.print(f"      [yellow]Review logged with API_Error indicators.[/yellow]")
                        continue  # Move to next datasheet
                        
                    elif not scores_dict:
                        # If no scores could be extracted and it wasn't an API error, raise exception
                        raise ValueError("Failed to extract any scores from the LLM response")
                        
                    logger.info(f"Successfully parsed review data with {len(scores_dict)} scores for {gen_ds_path}")
                    
                    # Calculate Average_Pn_Score
                    p_scores = []
                    for i in range(1, 17):
                        p_key = f"P{i}"
                        if p_key in scores_dict and isinstance(scores_dict[p_key], (int, float)):
                            p_scores.append(scores_dict[p_key])
                    
                    if p_scores:
                        average_pn_score = sum(p_scores) / len(p_scores)
                        scores_dict['Average_Pn_Score'] = round(average_pn_score, 2)
                    else:
                        scores_dict['Average_Pn_Score'] = "N/A"

                    review_logger.log_review(
                        reviewer_provider=reviewer_llm_provider_name_val,
                        reviewer_model=reviewer_llm_model_name_simple_val,
                        sensor_brand=current_brand,
                        sensor_type=current_sensor_type,
                        generator_provider=generated_model_provider,
                        generator_model=generated_model_name_simple,
                        official_datasheet_status=official_datasheet_status,
                        scores=scores_dict,
                        justifications=justifications_dict
                    )
                    console.print(f"      [green]✓ Review scores extracted and logged successfully.[/green]")
                except Exception as e:
                    logger.error(f"Error processing review data for {gen_ds_path}: {e}", exc_info=True)
                    console.print(f"      [red]Error processing review data: {e}.[/red]")

    console.print("\n[bold green]Review process completed for all selected sensors and models.[/bold green]")
    logger.info("Review process finished.")

if __name__ == '__main__':
    cli()