# THIS WORKS!
# %%
# packages importing
import pandas as pd
import requests
from openai import OpenAI
from bs4 import BeautifulSoup

# %%
df_gamma = pd.read_csv('../data/4053423225952_specifications.csv')
spec_names = df_gamma.columns
specs = df_gamma
print("-------------------------")
print(spec_names, "\nEAN is", df_gamma['EAN'][0])
print("-------------------------")

# %%

#print(df_gamma)


# Set up prompt for ChatGPT
prompt = f"""
What can you tell me about the EAN named as {df_gamma['EAN'][0]}?
You can check if its attributes are correct at attributes at:{df_gamma.to_markdown()}
Specifically, can you make a bulletpoint of how many of the specifications I provide are correct and how many are wrong?

Could you also tell me what percentage of information I provided is correct? 

For instance if I gave 20 specifications and 16 of them are correct can you say:
- From the information you gave 80% is correct!

"""

# print(prompt)
#
# # Connect to ChatGPT with the new API call
# response = OpenAI.ChatCompletion.create(
#     model='gpt-4',  # Adjust model if needed
#     messages=[
#         {'role': 'system', 'content': 'You are a football scout'},
#         {'role': 'user', 'content': prompt}
#     ]
# )
#
# print(response['choices'][0]['message']['content'])

client = OpenAI(api_key="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")

model = 'gpt-4o'
temperature = 0.7
max_tokens = 1000

messages = [
    {'role': 'system', 'content': 'you are a helpful assistant'},
    {'role': 'user', 'content': prompt}
]

# helper function
def get_summary():
    completion = client.chat.completions.create(
        model = model,
        messages = messages,
        temperature = temperature,
        max_tokens = max_tokens
    )
    return completion.choices[0].message.content

print(get_summary())