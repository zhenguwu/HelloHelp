import pyautogui
import requests
from io import BytesIO

# Capture the screenshot
screenshot = pyautogui.screenshot()

# Save the screenshot to a BytesIO object (in-memory file)
img_bytes = BytesIO()
screenshot.save(img_bytes, format='PNG')
img_bytes.seek(0)  # move to the beginning of the BytesIO object

f = open('screenshot.png', 'rb')

# Define the API endpoint
url = 'http://localhost:5000/'

# Define the user ID
user_id = '12345'

# Create the files dictionary to simulate file upload
files = {'photo': ('screenshot.png', f, 'image/png')}

# Begin the help session
response = requests.post(url + 'begin', data={'user_id': user_id, 'task': "Book a reservation at a Angie's Pizza"})
print(response.text)

# Send the first POST request
response = requests.post(url + 'image', data={'user_id': user_id}, files=files)
print(response.text)

f = open('screenshot2.png', 'rb')
files = {'photo': ('screenshot2.png', f, 'image/png')}
#response = requests.post(url + 'image', data={'user_id': user_id}, files=files)
#print(response.text)