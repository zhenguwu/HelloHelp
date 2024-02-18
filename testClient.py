import pyautogui
import requests
from io import BytesIO

# Capture the screenshot
screenshot = pyautogui.screenshot()

# Save the screenshot to a BytesIO object (in-memory file)
img_bytes = BytesIO()
screenshot.save(img_bytes, format='PNG')
img_bytes.seek(0)  # move to the beginning of the BytesIO object

# Define the API endpoint
url = 'http://localhost:5000/'

# Define the user ID
user_id = '12345'

# Create the files dictionary to simulate file upload
files = {'photo': ('screenshot.png', img_bytes, 'image/png')}

# Begin the help session
response = requests.post(url + 'begin', data={'user_id': user_id})

# Send the first POST request
response = requests.post(url, data={'user_id': user_id}, files=files)

# Print the response from the server
print(response.text)