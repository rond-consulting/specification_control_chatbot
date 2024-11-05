#url = "https://www.gamma.nl/assortiment/bosch-18v-decoupeerzaag-pst18-zonder-accu/p/B391153"

from specification_scrape import scrape_specifications
import pandas as pd
from asking_chatgpt import check_specs, extract_data_dict_from_markdown
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access the API key
api_key = os.getenv("working_api")

# Confirm that it's accessible
if api_key:
    print("API Key found:", api_key)
else:
    print("API Key not found!")

url = "https://www.gamma.nl/assortiment/bosch-18v-decoupeerzaag-pst18-zonder-accu/p/B391153"
df_to_check = pd.read_csv("data/incorrect_specs.csv")
markdown_file = 'data/corrected_specs_summary.md'

def main():
    scrape_specifications(url)
    check_specs(df_to_check)
    extract_data_dict_from_markdown(markdown_file)


if __name__ == "__main__":
    main()
