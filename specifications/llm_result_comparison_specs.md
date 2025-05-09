# Feature Specification: LLM Result Comparison and Scoring

**Version:** 1.0
**Date:** May 6, 2025

## 1. Introduction

This document outlines the specification for a new feature that enables the comparison and scoring of LLM-generated sensor datasheets against official datasheets. The scoring will be performed by another LLM acting as a reviewer, using a 1-5 Likert scale.

## 2. Goals

*   To provide a quantitative measure of how accurately and comprehensively different LLMs can generate datasheets for various sensors.
*   To automate the comparison process using an LLM as a reviewer.
*   To output the comparison results in a structured CSV format for easy analysis.

## 3. Proposed Implementation Steps

### Step 1: Official Datasheet Loader

*   **Objective:** To load official datasheets for the sensors listed in `data/sensors.csv`.
*   **Details:**
    *   A new module/class (e.g., `OfficialDatasheetLoader` in `src/datasheet_loader.py`) will be responsible for:
        *   Reading the sensor information from `data/sensors.csv`, specifically the `Brand` and `Sensor` columns.
        *   Constructing the official datasheet filename in the format `[Brand]_[Sensor].md`.
        *   Loading the content of the official datasheet from the `datasheet` directory.
        *   Error handling for missing datasheets must be implemented. A status (e.g., "Official Datasheet Not Found") should be logged.
    *   The official datasheets are expected to be in Markdown format and stored in the `datasheet` directory.

### Step 2: LLM Reviewer Implementation

*   **Objective:** To use an LLM to review and score the previously generated datasheets against the official ones.
*   **Details:**
    *   **Review Prompt:** A new prompt template file (e.g., `prompts/review_criteria_prompt.txt`) will be created. This prompt will instruct the reviewer LLM to:
        *   Act as an expert technical reviewer.
        *   Compare a given "Generated Datasheet" against an "Official Datasheet".
        *   For each of the following criteria (P1-P16), provide a score on a 1-5 Likert scale (1 = Very Poor, 5 = Excellent) and a brief justification for each score.
        *   Finally, provide a single overall score on a 1-5 Likert scale (1 = Very Poor, 5 = Excellent) and an overall justification.
        *   **Review Criteria:**
            *   **P1. Disclaimer:** Check if the LLM-generated datasheet includes a disclaimer stating its unofficial nature, the lack of guaranteed accuracy, and the necessity to refer to the official manufacturer datasheet for critical applications.
            *   **P2. Manufacturer Info:** Verify if the LLM includes accurate manufacturer information, including the company name, website, and production details.
            *   **P3. General Description:** Compare the comprehensiveness and accuracy of the sensor's function and technology description.
            *   **P4. Theory of Operation / Sensing Principle:** Assess the explanation of how the sensor works, focusing on accuracy and detail.
            *   **P5. Features:** Evaluate key capabilities and selling points, noting any missing or incorrect information.
            *   **P6. Potential Applications:** Review common use cases, checking for completeness and relevance.
            *   **P7. Pin Configuration and Description:** Check for correct pin names, numbers, and functions.
            *   **P8. Absolute Maximum Ratings:** Compare stress ratings, ensuring no misinformation on damage thresholds.
            *   **P9. Electrical Characteristics:** Rate the detail level and accuracy of voltage levels, input/output characteristics, and the inclusion of a Power Consumption Breakdown for different modes.
            *   **P10. Operating Conditions:** Ensure the datasheets match on recommended supply voltage, temperature, and humidity ranges.
            *   **P11. Sensor Performance / Specifications:** Analyze key metrics like range, accuracy, resolution, sensitivity, response time, stability, etc., for accuracy and completeness.
            *   **P12. Communication Protocol / Interface:** Verify the description of communication methods, timings, and parameters.
            *   **P13. Register Map:** If applicable, compare the detail and accuracy of register-based configuration information.
            *   **P14. Package Information / Mechanical Dimensions:** Check for correct package descriptions and dimensions.
            *   **P15. Basic Usage / Application Information:** Rate the usefulness of connection diagrams, external components, and steps for sensor setup.
            *   **P16. Compliance and Certifications:** Ensure placeholders for common standards are included, noting the need for manufacturer verification.
        *   The prompt will clearly define the expected output format for all scores and justifications (e.g., a JSON object with keys like `p1_score`, `p1_justification`, ..., `p16_score`, `p16_justification`, `overall_score`, `overall_justification`) for easy parsing.
    *   **LLM Selection:** The user will be able to select which LLM model (from the existing `config.yaml` list) will act as the "reviewer LLM". This could be the same or different from the LLMs that originally generated the datasheets.
    *   **Process:**
        *   For each sensor (e.g., Brand: "Bosch", Type: "BME280") and each LLM-generated datasheet for that sensor (e.g., from `results/Bosch/BME280/anthropic_claude-3.5-haiku_20250504_030759.md`):
            1.  Fetch/load the official datasheet text for the sensor (from Step 1).
            2.  Load the text of the specific LLM-generated datasheet.
            3.  Construct the review prompt using the official text, the generated text, and the P1-P16 scoring criteria.
            4.  Send the prompt to the selected reviewer LLM (e.g., "google_gemini-1.5-pro") using the existing `APIClient` infrastructure.
            5.  Parse the reviewer LLM's response to extract all scores (P1-P16, overall) and justifications for this specific generated datasheet.
            6.  Pass this complete set of review data (sensor info, generator LLM info, reviewer LLM info, scores, justifications) to the `ReviewScoreLogger`.

### Step 3: Output CSV File

*   **Objective:** To store the comparison scores in structured CSV files, organized by reviewer LLM and then by sensor.
*   **Details:**
    *   CSV files will be generated or appended to under a base directory, e.g., `results/reviews/`.
    *   For each **reviewer LLM**, a subdirectory will be created using its provider and model name, e.g., `results/reviews/[ReviewerLLMProvider]_[ReviewerLLMModel]/`.
        *   Example: `results/reviews/google_gemini-1.5-pro/`
    *   Within each reviewer LLM's directory, a separate CSV file will be created for **each sensor** that is reviewed. The CSV filename will be `[SensorBrand]_[SensorType].csv`.
        *   Example: `results/reviews/google_gemini-1.5-pro/Bosch_BME280.csv`
    *   Each row in such a CSV file will represent the review of a single **LLM-generated datasheet** for that specific sensor, performed by that specific reviewer LLM.
    *   The CSV file will have the following columns:
        *   `Sensor_Brand`
        *   `Sensor_Type`
        *   `Generated_Datasheet_LLM_Provider` (e.g., "openrouter", "google_gemini", "anthropic")
        *   `Generated_Datasheet_LLM_Model` (e.g., "claude-3.5-haiku", "gpt-4", "gemini-1.5-pro")
        *   `Reviewer_LLM_Provider` (This will be consistent for all rows within files in the same reviewer model directory)
        *   `Reviewer_LLM_Model` (This will be consistent for all rows within files in the same reviewer model directory)
        *   `Official_Datasheet_Status` (e.g., "Found", "Not Found", "Error Fetching", "Not Specified")
        *   `P1_Disclaimer_Score` (1-5 or N/A)
        *   `P2_Manufacturer_Info_Score` (1-5 or N/A)
        *   `P3_General_Description_Score` (1-5 or N/A)
        *   `P4_Theory_Of_Operation_Score` (1-5 or N/A)
        *   `P5_Features_Score` (1-5 or N/A)
        *   `P6_Potential_Applications_Score` (1-5 or N/A)
        *   `P7_Pin_Configuration_Score` (1-5 or N/A)
        *   `P8_Absolute_Maximum_Ratings_Score` (1-5 or N/A)
        *   `P9_Electrical_Characteristics_Score` (1-5 or N/A)
        *   `P10_Operating_Conditions_Score` (1-5 or N/A)
        *   `P11_Sensor_Performance_Score` (1-5 or N/A)
        *   `P12_Communication_Protocol_Score` (1-5 or N/A)
        *   `P13_Register_Map_Score` (1-5 or N/A)
        *   `P14_Package_Information_Score` (1-5 or N/A)
        *   `P15_Basic_Usage_Score` (1-5 or N/A)
        *   `P16_Compliance_Certifications_Score` (1-5 or N/A)
        *   `Average_Pn_Score` (Average of P1-P16 scores, or N/A)
        *   `Overall_Likert_Score` (The single 1-5 overall score from the LLM, or N/A)
        *   `P1_Justification` (Text)
        *   `P2_Justification` (Text)
        *   ... (up to P16_Justification)
        *   `P16_Justification` (Text)
        *   `Overall_Justification` (Text)
        *   `Review_Timestamp` (YYYY-MM-DD HH:MM:SS)
    *   A new module/class (e.g., `ReviewScoreLogger` in `src/review_logger.py`) will handle creating the directory structure and writing to these CSV files, including header creation if a CSV file doesn't exist or is new.

## 4. User Interface

*   **Objective:** To provide a command-line interface for initiating the review process.
*   **Details:**
    *   A new `click` command will be added to `src/main.py`, for example, `review-datasheets`.
    *   This command will allow the user to:
        *   Select the LLM model to act as the reviewer (from `config.yaml`).
        *   Optionally, specify filters for which generated datasheets to review (e.g., by original generator LLM, by sensor). Default to reviewing all available generated datasheets for which official datasheets can be found.
        *   Trigger the review and scoring process.
    *   The command will utilize the `OfficialDatasheetLoader`, `APIClient`, and `ReviewScoreLogger` components.

## 5. Error Handling and Logging

*   Robust error handling for:
    *   Unavailable official datasheets.
    *   Failures in downloading/parsing official datasheets.
    *   Failures in the reviewer LLM API calls.
    *   Failures in parsing the reviewer LLM's response (especially the score).
*   Errors and statuses should be logged appropriately (e.g., to the console and/or a dedicated log file).

## 6. Future Considerations

*   Allowing users to define custom review criteria in the prompt.
*   Support for multiple reviewers and aggregation of scores.
*   More sophisticated parsing of reviewer LLM output if it's free-form text.
*   Comparing different versions of generated datasheets for the same sensor/LLM.