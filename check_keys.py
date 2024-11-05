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
