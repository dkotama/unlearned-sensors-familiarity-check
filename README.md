# Unlearned Sensors Project

This is the main repository for the Unlearned Sensors project, a tool for comparing responses from different Large Language Models (LLMs) about sensor datasheets.

## Setup

1. **Install Dependencies**: Ensure you have Python 3 and the required packages installed. Run `pip install -r requirements.txt` to set up the necessary libraries.
2. **Install Pandoc**: For PDF conversion of generated markdown files, you need to have 'pandoc' installed on your system. Visit [https://pandoc.org/installing.html](https://pandoc.org/installing.html) for installation instructions.
3. **Configuration**: Adjust settings in `config/config.yaml` as needed, including API keys and paths.

## Usage

1. **Run the Comparison Tool**: Execute `python src/main.py run` to start the interactive CLI tool. Follow the prompts to select sensors and models for comparison.
2. **Results**: Generated markdown (.md) files with LLM responses will be saved in the `results/` directory, organized by sensor type.
3. **PDF Conversion**: After all markdown files are generated, the tool automatically converts them to PDF format using 'pandoc' and saves them in the `pdf/` directory with a similar subfolder structure.
4. **Manual PDF Conversion**: If needed, you can run `python src/main.py convert-pdf` to manually convert existing .md files to PDF, useful in case of errors during the initial conversion.