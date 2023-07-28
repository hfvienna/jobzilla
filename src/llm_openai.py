import os

import openai

from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]


def llm(system_message, user_message):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": system_message,
            },
            {"role": "user", "content": user_message},
        ],
    )
    # Extract the message content from the first choice
    completion = response["choices"][0]["message"]["content"]
    return completion