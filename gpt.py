from openai import OpenAI
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = os.getenv('OPENAI_API_KEY')

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {API_KEY}"
}

def generate_message(text, base64_image=None):
    return {
        "role": "system",
        "content": text
    }

def gpt_chat_completion(messages, model="gpt-4-vision-preview", temperature=1, max_tokens = None):
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if max_tokens is not None:
        data["max_tokens"] = max_tokens

    response = requests.post(API_ENDPOINT, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")