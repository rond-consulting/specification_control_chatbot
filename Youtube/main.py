from openai import OpenAI, api_key
import os
#import PyPDF2
from dotenv import load_dotenv, find_dotenv
import prompts
from Youtube.prompts import system_message

_ = load_dotenv(find_dotenv())

#client = OpenAI(api_key=os.environ.get('OPEN_API_KEY'))
#client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))
client = OpenAI(api_key="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")


model = 'gpt-3.5-turbo'
temperature = 0.3
max_tokens = 500
topic = ""

# read the pdf
book = ""

system_message = prompts.system_message
prompt = prompts.generate_prompt(book, topic)
messages = [
    {'role': 'system', 'content': 'you are a helpful assistant'},
    {'role': 'user', 'content': 'tell me 10 facts about AI'}
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

#
# from openai import OpenAI
#
# client = OpenAI()
#
# stream = client.chat.completions.create(
#     model="gpt-4o-mini",
#     messages=[{"role": "user", "content": "Say this is a test"}],
#     stream=True,
# )
# for chunk in stream:
#     if chunk.choices[0].delta.content is not None:
#         print(chunk.choices[0].delta.content, end="")