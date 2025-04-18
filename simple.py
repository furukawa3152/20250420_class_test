import os

from openai import OpenAI

client = OpenAI(api_key = os.environ["API_KEY"])

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "日本語で回答してください。"},
        {"role": "user", "content": "Pythonとは"}
    ])

print(response.choices[0].message.content)
