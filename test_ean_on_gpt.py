import pandas as pd
import requests
from openai import OpenAI
from bs4 import BeautifulSoup

# %%
df_gamma = pd.read_csv('4053423225952_specifications.csv')
spec_names = df_gamma.columns
specs = df_gamma
print("-------------------------")
print(spec_names, "\nEAN is", df_gamma['EAN'][0])
print("-------------------------")

# %%

#print(df_gamma)


# Set up prompt for ChatGPT
prompt = (f"What can you tell me about the EAN named as {df_gamma['EAN'][0]}? "
          f"You can check if its attributes are correct at attributes at:\n{df.to_markdown()}")

print(prompt)

# Connect to ChatGPT with the new API call
response = OpenAI.ChatCompletion.create(
    model='gpt-4',  # Adjust model if needed
    messages=[
        {'role': 'system', 'content': 'You are a football scout'},
        {'role': 'user', 'content': prompt}
    ]
)

print(response['choices'][0]['message']['content'])
