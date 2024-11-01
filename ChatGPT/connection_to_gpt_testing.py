import openai
import os

openai.api_key = os.getenv('api_key_personal_laptop')


#api_key_axians_laptop = "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"

#openai.api_key = api_key_axians_laptop
#client = openai(api_key=api_key_axians_laptop)

try:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "Hello"}]
    )
    print(response.choices[0].message.content)
except Exception as e:
    print(f"An error occurred: {e}")

