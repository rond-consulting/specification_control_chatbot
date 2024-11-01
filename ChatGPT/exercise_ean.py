import pandas as pd
import requests
from openai import OpenAI
from bs4 import BeautifulSoup
import numpy as np

# Set your OpenAI API key
secret_api_key = "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"
api_key_personal_laptop = "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"


client = OpenAI(api_key=api_key_personal_laptop)

response = client.models.list()
print("printing response")
print(response)


player_name = 'Lamine Yamal'
url = 'https://fbref.com/en/players/82ec26c1/Lamine-Yamal'
attrs = 'scout_summary_AM'

# Scrape the table
df = pd.read_html(url, attrs={'id': attrs})[0]
print(df)

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

df = df.dropna(subset='Statistic')

prompt = f"""
I need a scout report for player {player_name}
Here are his attributes:
{df.to_markdown()}

Return the following in markdown format:
Report for {player_name}:
Strengths:
<a list of 1-2 strengths>

Weakness:
<a list of 1-2 weakness>


"""

response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # Using gpt-3.5-turbo if gpt-4 is unavailable
    messages=[
        {'role': 'system',
         'content': 'you are a professional football scout'},
        {'role': 'user',
         'content': prompt}
    ],
)


print(response.choices[0].message.content)

with open(f'/Users/baranmetin/Desktop/Data Sciences Exercises/EAN_matching/'
          f'{player_name}_report.md', 'w') as f:
    f.write(response.choices[0].message.content)
print(prompt)
print("end of chatgpt")

