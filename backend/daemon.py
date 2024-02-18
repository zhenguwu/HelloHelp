import pyautogui
import requests
from io import BytesIO
import time
import json
import sys

# Define the API endpoint
url = 'http://localhost:5000/'

# Define the user ID
user_id = '12345'

def start_help(task):
    # Begin the help session
    response = requests.post(url + 'begin', data={'user_id': user_id, 'task': task})

def add_image():
    # Take a screenshot
    screenshot = pyautogui.screenshot()

    screen_width, screen_height = screenshot.size
    crop_area = (0, 0, screen_width // 3 * 2, screen_height)

    screenshot = screenshot.crop(crop_area)

    # Save the screenshot to a BytesIO object (in-memory file)
    img_bytes = BytesIO()
    screenshot.save(img_bytes, format='PNG')
    img_bytes.seek(0)  # move to the beginning of the BytesIO object

    # Create the files dictionary to simulate file upload
    files = {'photo': ('screenshot.png', img_bytes, 'image/png')}

    # Send the first request
    response = requests.post(url + 'image', data={'user_id': user_id}, files=files)
    response = json.loads(response.text)
    print(response["briefExplanation"])

def add_images():
    while (True):
        time.sleep(3)
        # Capture the screenshot
        screenshot = pyautogui.screenshot()

        # Save the screenshot to a BytesIO object (in-memory file)
        img_bytes = BytesIO()
        screenshot.save(img_bytes, format='PNG')
        img_bytes.seek(0)  # move to the beginning of the BytesIO object

        # Create the files dictionary to simulate file upload
        files = {'photo': ('screenshot.png', img_bytes, 'image/png')}

        # Send the first request
        response = requests.post(url + 'image', data={'user_id': user_id}, files=files)
        print(response.text)

        x = input("Press enter to continue")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Hardcode task for testing purposes
        start_help("Set my computer to dark mode")
        add_images()
    else:
        arg1 = sys.argv[1]
        if arg1 == "1":
            start_help(sys.argv[2])
            add_image()
        elif arg1 == "2":
            add_image()        