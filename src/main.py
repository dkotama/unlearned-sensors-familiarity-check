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

from src.api_client import OpenRouterClient
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
    
    for idx, model in enumerate(models):
        table.add_row(str(idx), model)
    
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
    client = OpenRouterClient(cfg['openrouter_api_key'], cfg['api_base_url'], cfg['request_timeout'])
    prompt_gen = PromptGenerator(cfg['prompt_template_path'])
    result_proc = ResultProcessor(cfg['results_base_path'])
    metrics_logger = MetricsLogger(cfg['metrics_log_path'])
    
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
            
            for model in selected_models:
                completed += 1
                status.update(f"[bold green]Processing request {completed}/{total_requests}: {sensor_brand} {sensor_type} with {model}[/bold green]")
                
                # Send request to model
                start_time = datetime.now()
                try:
                    response = client.send_request(model, prompt)
                    end_time = datetime.now()
                    
                    response_time = (end_time - start_time).total_seconds()
                    input_tokens = response.get('input_tokens', 0)
                    output_tokens = response.get('output_tokens', 0)
                    response_text = response.get('text', '')
                    response_length = len(response_text)
                    
                    # Save result
                    result_filename = result_proc.save_result(sensor_brand, sensor_type, model, response_text)
                    
                    # Log metrics
                    metrics_logger.log_metrics(
                        sensor_brand, sensor_type, model, 
                        response_time, input_tokens, output_tokens, response_length
                    )
                    
                    console.print(f"[green]✓ Completed {completed}/{total_requests}: {sensor_brand} {sensor_type} with {model} (saved to {result_filename})[/green]")
                except Exception as e:
                    console.print(f"[red]✗ Error on {completed}/{total_requests}: {sensor_brand} {sensor_type} with {model}: {str(e)}[/red]")
    
    console.print("[bold green]All requests completed![/bold green]")

if __name__ == '__main__':
    cli()