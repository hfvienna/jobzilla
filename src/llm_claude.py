import os

import anthropic
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["ANTHROPIC_API_KEY"]

anthropic_client = anthropic.Client(api_key=api_key)


def llm(system_message, user_message):
    completion = anthropic_client.completion(
        model="claude-2",
        max_tokens_to_sample=2000,
        prompt="\n\nHuman:" + system_message + user_message + "\n\nAssistant:",
        temperature=0.0,
    )
    return completion