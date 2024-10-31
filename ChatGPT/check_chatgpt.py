import os
import openai
import certifi

# Set your API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Verify that the API key was retrieved
if openai.api_key is None:
    raise ValueError("API key not found. Please set the OPENAI_API_KEY environment variable.")

# Your prompt
prompt = "What is the world's most delicious cake?"

# Create a chat completion
try:
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use "gpt-3.5-turbo" if you don't have access to GPT-4
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7,
    )

    # Get the assistant's reply
    reply = response.choices[0].message['content']

    # Save the reply to a Markdown file
    with open('response.md', 'w', encoding='utf-8') as file:
        file.write(reply)

    print("Response saved to response.md")

except openai.OpenAIError as e:
    print(f"An error occurred: {e}")
