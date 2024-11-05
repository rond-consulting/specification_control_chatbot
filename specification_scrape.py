# The function to scrape the information from given website

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

def scrape_specifications(url: str):
    # URL of the product page

    # Send a request to the webpage
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract specifications under the "Specificaties" header
    specifications = {}

    # Find the specifications section
    spec_section = soup.find("div", {"id": "product-specifications"})

    if spec_section:
        # Extract each specification
        for row in spec_section.find_all("tr"):
            # Each row should contain a label and a value
            label_cell = row.find("th")
            value_cell = row.find("td")

            # Check if both label and value exist
            if label_cell and value_cell:
                label = label_cell.get_text(strip=True)
                value = value_cell.get_text(strip=True)
                specifications[label] = value

        # Retrieve the EAN number to use as the main name
        ean_number = specifications.get("EAN", "unknown")

        # Save specifications as a DataFrame
        df = pd.DataFrame([specifications], index=[ean_number])
        print("DataFrame:")
        print(df)

        # Save DataFrame to CSV (optional)
        df.to_csv("data/incorrect_specs.csv", index=False)

    else:
        print("Specifications section not found on the page.")

url = "https://www.gamma.nl/assortiment/bosch-18v-decoupeerzaag-pst18-zonder-accu/p/B391153"
scrape_specifications(url)
print('Specs are stored successfully!')