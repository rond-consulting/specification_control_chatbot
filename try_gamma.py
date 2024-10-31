import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

# URL of the product page
url = "https://www.gamma.nl/assortiment/bosch-18v-decoupeerzaag-pst18-zonder-accu/p/B391153"

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
    df.to_csv(f"{ean_number}_specifications.csv", index=False)

    # Save specifications as JSON with EAN as the main name
    with open(f"{ean_number}_specifications.json", "w") as json_file:
        json.dump({ean_number: specifications}, json_file, indent=4)

    print(
        f"Specifications saved as {ean_number}_specifications.csv and {ean_number}_specifications.json")
else:
    print("Specifications section not found on the page.")


df_bosch = pd.read_csv('/data/4053423225952_specifications.csv')
print(df_bosch.dtypes)