# %%
# packages importing
from openai import OpenAI, api_key
import prompts
import pandas as pd
import re
import os
from dotenv import load_dotenv

load_dotenv()

# Access the API key
api_key = os.getenv("private_api")

# # Confirm that it's accessible
# if api_key:
#     print("API Key found:", api_key)
# else:
#     print("API Key not found!")

def check_specs(df):


    ean = df['EAN'][0]
    # Set up prompt for ChatGPT
    prompt = f"""

    What can you tell me about the EAN named as {ean}?
    
    Can you please give me the correct values of the specifications for the following specs: {df.columns}
    You can check if its attributes are correct at attributes at:
    {df.to_markdown()}

    Please give the results in a dataframe illustration with 'data' as the variable name and key value pairs as specifications and their respective values. The variable name needs to be 'data'

"""


    #client = OpenAI(api_key=os.environ.get('working_api'))
    api_key = os.getenv("private_api")

    if api_key is None:
        raise ValueError("API Key not found. Please set the MY_API_KEY environment variable.")

    client = OpenAI(api_key=api_key)
    system_message = prompts.system_message


    model = 'gpt-4o-mini'
    temperature = 0.7
    max_tokens = 1000

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': prompt}
    ]

    # helper function
    def get_summary():
        # ean = ean,
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return completion.choices[0].message.content

    # Fetch the summary with corrections in markdown format
    summary = get_summary()

    # Ensure the summary is markdown-formatted by adding headers if necessary
    markdown_content = "### Corrected Specifications Summary\n\n" + summary

    # Save the markdown response to a .md file
    with open("data/corrected_specs_summary.md", "w", encoding="utf-8") as file:
        file.write(markdown_content)

    print(f"To do this job I used {model} as the base model")
    print("Markdown summary saved as 'corrected_specs_summary.md'")
    print(summary)

    return summary

df_incorrect =pd.read_csv('data/incorrect_specs.csv')
check_specs(df_incorrect)



def extract_data_dict_from_markdown(file_path):
    # Step 1: Read the markdown file
    with open(file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()

    # Step 2: Extract the data dictionary using regex
    md_file_clean = re.search(r"data\s*=\s*\{(.+?)\}\s*", md_content, re.DOTALL)

    if md_file_clean:
        # Extract the matched content and strip leading/trailing whitespace
        data_dict_str = md_file_clean.group(1).strip()

        # Debugging: print the extracted dictionary string
        print("Extracted data dictionary string:", data_dict_str)

        try:
            # Step 3: Evaluate the string to convert it to a dictionary
            data_dict = eval('{' + data_dict_str + '}')  # Evaluate the extracted dictionary string

            # Convert the dictionary to a DataFrame
            correct_df = pd.DataFrame(
                [data_dict])  # Wrap in a list to create a DataFrame with one row

            # Save DataFrame to CSV
            correct_df.to_csv("data/correct_specs.csv", index=False)
            print("Data successfully saved to data/correct_specs.csv")

        except Exception as e:
            print("Error during evaluation or saving:", e)
    else:
        print("Data dictionary pattern not found in the markdown file.")


# Call the function
md_file = 'data/corrected_specs_summary.md'
extract_data_dict_from_markdown(md_file)

print("all files are exported successfully!")