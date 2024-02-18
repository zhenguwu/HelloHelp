from openai import OpenAI
import requests
import json
import os
from dotenv import load_dotenv
import json

load_dotenv()
API_ENDPOINT = "https://api.openai.com/v1/chat/completions"
API_KEY = os.getenv('OPENAI_API_KEY')
UPLOAD_FOLDER = 'user_data/'
INSTRUCTIONS = '''You are a guiding tool to help people navigate through user interfaces on a computer to accomplish a task.
All future messages will be continual screenshots of the user interface. Previous screenshots will not be shown again.
You will provide step by step instructions, one action at a time, to help the user accomplish the task.
## Task
{task}

## Action Format
type ClickAction = {{ "action": "click", "text": string }}
type TypeAction = {{ "action": "type", "text": string }}
type ScrollAction = {{ "action": "scroll", "direction": "up" | "down" }}
type RequestInfoFromUser = {{ "action": "request", "prompt": string }}
type Done = {{ "action": "done" }}

For ClickAction, the text field is the exact text of the button or link to click. Do not assume the user can click on anything without explicit instruction. Search bars must be clicked on before typing.


## JSON Response Format
{{
  "briefExplanation": string,
  "nextAction": ClickAction | TypeAction | ScrollAction | RequestInfoFromUser | Done
}}

Do not add any additional text to the response.
'''


headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {API_KEY}"
}

### Helper Methods ###

def save_messages_to_file(messages, user_id):
    filename = f"{UPLOAD_FOLDER}{user_id}/{user_id}_history.json"
    with open(filename, 'w') as file:
        json.dump(messages, file, indent=4)

# TODO, cut out oldest images when low on tokens
def read_messages_from_file(user_id):
    filename = f"{UPLOAD_FOLDER}{user_id}/{user_id}_history.json"
    try:
        with open(filename, 'r') as file:
            history = json.load(file)
            return history
    except FileNotFoundError:
        # Return an empty list if the file doesn't exist
        return []
    
def generate_message(text='', message=None, base64_image=None):
    if (base64_image is not None):
        return {
            "role": "user",
            "content": [{
                "type": "image_url",
                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
            }]
        }
    if (message is not None):
        return {
            "role": "user",
            "content": message
        }
    return {
        "role": "system",
        "content": text
    }

### Main Methods ###

# Initate the help session by creating a folder for the user and clearing any existing history. Adds a new system messsage with instructions
def begin_help(user_id, task):
    os.makedirs(UPLOAD_FOLDER + user_id, exist_ok=True)
    for file in os.scandir(UPLOAD_FOLDER + user_id):
        os.unlink(file.path)
    save_messages_to_file([generate_message(INSTRUCTIONS.format(task=task))], user_id)

# Continue the help session by adding the next image and calling the GPT-4 API
def add_image(user_id, base64_image):
    # Read the messages from file and add the new image
    messages = read_messages_from_file(user_id)
    messages.append(generate_message(base64_image=base64_image))
    
    # Call the GPT-4 API
    print("Calling GPT...")
    response = gpt_chat_completion(messages)
    
    # Remove the image from the message
    messages[-1]["content"] = []

    # Add the response to the message and save to file
    messages.append(response)
    save_messages_to_file(messages, user_id)

    try:
        response = json.loads(response["content"])
    except:
        print("Response is not valid JSON")
        print(response)
        return None
    return response

# Continue the help session by adding the next message and calling the GPT-4 API
def add_message(user_id, message):
    # Read the messages from file and add the new message
    messages = read_messages_from_file(user_id)
    messages.append(generate_message(message=message))

    # Call the GPT-4 API
    print("Calling GPT...")
    response = gpt_chat_completion(messages)

    print(response)


def gpt_chat_completion(messages, model="gpt-4-vision-preview", temperature=0.2, max_tokens=4096):
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    response = requests.post(API_ENDPOINT, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")