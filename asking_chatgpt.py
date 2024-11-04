# THIS WORKS!
# %%
# packages importing
from openai import OpenAI
import prompts
import markdown
import pandas as pd
import re



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
    client = OpenAI(api_key="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")

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
    with open("corrected_specs_summary.md", "w", encoding="utf-8") as file:
        file.write(markdown_content)

    print(f"To do this job I used {model} as the base model")
    print("Markdown summary saved as 'corrected_specs_summary.md'")
    print(summary)

    return summary

df = pd.read_csv("data/incorrect_specs.csv")
check_specs(df)


def extract_data_dict_from_markdown(file_path):
    # Step 1: Read the markdown file
    with open(file_path, 'r', encoding='utf-8') as file:
        md_content = file.read()

    # Step 2: Extract the data dictionary using regex
    md_file_clean = re.search(r"data\s*=\s*pd\.DataFrame\s*\(\s*\{(.+?)\}\s*\)", md_content, re.DOTALL)

    if md_file_clean:
        # Extract the matched content and strip leading/trailing whitespace
        data_dict_str = md_file_clean.group(1).strip()

        # Step 3: Evaluate the string to convert it to a dictionary
        data_dict = eval('{' + data_dict_str + '}')  # Evaluate the extracted dictionary string

        # Convert the dictionary to a DataFrame
        correct_df = pd.DataFrame(data_dict)

        correct_df.to_csv(f"data/correct_specs.csv", index=False)

md_file = 'corrected_specs_summary.md'
extract_data_dict_from_markdown(md_file)