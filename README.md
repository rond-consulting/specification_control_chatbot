# Product EAN Check Project

## Overview
This project leverages OpenAI's ChatGPT model to validate and retrieve product specifications based on EAN (European Article Number) codes for Gamma products. 

It scrapes specification data from a given URL, queries ChatGPT for verification, and compares the returned specifications against the scraped data. A Streamlit interface is provided to visually compare specifications from the Gamma website and ChatGPT responses.

Before starting the project, make sure to have an OpenAI API key that you can use in this project

## Project Structure

- **`main.py`**: The main Python script that runs the necessary files to:
  - scrape actual information from Gamma.nl
  - Ask a prompt to retrieve the correct information from ChatGPT.
  - Save the results from ChatGPT as a markdown file
  - Extract the ChatGPT results into a dataframe
- **`asking_chatgpt.py`**: Main Python script that:
  - Scrapes product specifications from the specified Gamma website URL.
  - Queries ChatGPT to validate and correct the specifications.
  - Saves the corrected specifications as a markdown summary.
- **`streamlit/`**: Directory containing Streamlit code for a web-based interface that:
  - Displays original and corrected specifications.
  - Compares data fields and calculates matching percentages.
  - Visualizes overall and per-field match percentages in pie and bar charts.
- **`data/`**: Directory storing data files:
  - `incorrect_specs.csv`: Specifications scraped from the Gamma website.
  - `corrected_specs_summary.md`: Specifications returned by ChatGPT.
  - `correct_specs.csv`: CSV file of the corrected data extracted from the ChatGPT response.

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set up environment variables:**
   - Create a `.env` file in the root directory and add your OpenAI API key:
     ```plaintext
     working_api=<your_openai_api_key>
     ```

3. **Install dependencies:**
   - Install the required packages from `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

## Usage

### 1. Run the main script

To scrape specifications from a product page, validate them with ChatGPT, and save the results:
```bash
python asking_chatgpt.py
```

### 2. Launch the Streamlit app

To visualize and compare specifications, run the following in the `streamlit` directory:
```bash
streamlit run app.py
```

### 3. Key Features

- **Scrape Specifications**: Extracts product details from the Gamma website.
- **ChatGPT Verification**: Validates specifications using ChatGPT.
- **Data Comparison**: Shows matches and mismatches between original and ChatGPT-corrected specifications.
- **Visualization**: Displays a pie chart for overall match percentage and a bar chart for specification-level match percentages.

## File Descriptions

- **`asking_chatgpt.py`**: The primary script that:
  - Loads environment variables.
  - Scrapes product specifications using BeautifulSoup.
  - Queries ChatGPT with EAN codes to verify and correct the specifications.
  - Saves the corrected specifications in markdown format.
  - Includes a helper function to extract data as a CSV file.
  
- **`streamlit/app.py`**: Streamlit application that:
  - Loads both original and corrected specifications.
  - Provides a user interface for comparing and visualizing specification match percentages.

## Environment Setup

This project uses a `.env` file for managing sensitive keys. Add the following environment variable to the `.env` file:
```plaintext
working_api=<your_openai_api_key>
```

## Dependencies

The `requirements.txt` file includes all the necessary packages:
- `openai`
- `dotenv`
- `pandas`
- `beautifulsoup4`
- `requests`
- `streamlit`
- `matplotlib`

## Notes

- Ensure that your `data/` folder contains the files `incorrect_specs.csv` and `correct_specs.csv` after running the script.
- The key column for comparison in the Streamlit app is `EAN`. If this column is not present in both datasets, an error will be shown.

## License

This project is licensed under the MIT License.
