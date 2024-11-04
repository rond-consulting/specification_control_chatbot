import pandas as pd
from openai import OpenAI
import gradio as gr
import prompts

system_message = prompts.system_message

client = OpenAI(api_key="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")
messages = [
    {'role': 'system', 'content': system_message}
]

def webapp_ean(user_input):
    messages.append({'role': 'user', 'content': user_input})
    model = 'gpt-3.5-turbo'
    temperature = 0.7
    max_tokens = 1000

    # Construct the prompt
    prompt = f"""
    What can you tell me about the EAN named as {user_input}?

    Specifically, can you make a list with bullet points of how many of the specifications does this EAN have?
    """

    # Append the prompt to the messages
    messages.append({'role': 'assistant', 'content': prompt})

    # Call the OpenAI API
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature
    )

    # Correctly access the content from the response
    ChatGPT_reply = response.choices[0].message.content  # Access content directly
    messages.append({'role': 'assistant', 'content': ChatGPT_reply})  # Store the reply

    return ChatGPT_reply

demo = gr.Interface(fn=webapp_ean, inputs='text', outputs='text', title='EAN Check')

demo.launch()
