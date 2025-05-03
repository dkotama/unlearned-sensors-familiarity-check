#!/usr/bin/env python3
"""
Main entry point for the LLM Sensor Knowledge Comparison application.
This CLI tool allows users to compare responses from different LLMs about sensor datasheets.
"""

import click
import pandas as pd
import yaml
from rich.console import Console
from rich.table import Table
import os
import sys
from datetime import datetime

# Add the parent directory to sys.path to import other modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api_client import APIClientFactory
from src.prompt_generator import PromptGenerator
from src.result_processor import ResultProcessor
from src.metrics_logger import MetricsLogger

console = Console()

def load_config(config_path):
    """Load configuration from YAML file."""
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def display_sensors(df):
    """Display available sensors in a table."""
    table = Table(title="Available Sensors")
    table.add_column("Index", style="cyan")
    table.add_column("Brand", style="magenta")
    table.add_column("Type", style="green")
    
    for idx, row in df.iterrows():
        table.add_row(str(idx), row['Brand'], row['Type'])
    
    console.print(table)

def display_models(models):
    """Display available models in a table."""
    table = Table(title="Available Models")
    table.add_column("Index", style="cyan")
    table.add_column("Model ID", style="magenta")
    table.add_column("Provider", style="green")
    
    for idx, model in enumerate(models):
        table.add_row(str(idx), model['id'], model['provider'])
    
    console.print(table)

@click.group()
def cli():
    """LLM Sensor Knowledge Comparison Tool"""
    pass

@cli.command()
@click.option('--config', default='config/config.yaml', help='Path to configuration file')
def run(config):
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
    console.print("[bold blue]Starting PDF conversion of .md files using pandoc...[/bold blue]")
    convert_to_pdf(cfg)

@cli.command()
@click.option('--config', default='config/config.yaml', help='Path to configuration file')
def convert_pdf(config):
    """Convert existing .md files in results directory to PDF."""
    cfg = load_config(config)
    console.print("[bold blue]Starting manual PDF conversion of .md files...[/bold blue]")
    convert_to_pdf(cfg)

def convert_to_pdf(cfg):
    """Convert .md files to PDF using pandoc."""
    import subprocess
    import glob
    
    results_path = cfg['results_base_path']
    pdf_base_path = os.path.join(os.path.dirname(results_path), 'pdf')
    
    # Ensure the base pdf directory exists
    os.makedirs(pdf_base_path, exist_ok=True)
    
    # Find all .md files in results directory and subdirectories
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

if __name__ == '__main__':
    cli()