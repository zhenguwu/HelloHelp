from flask import Flask, request, jsonify
#from werkzeug.utils import secure_filename
import os
from io import BytesIO
import base64
import gpt
import vision

app = Flask(__name__)

# Configure the upload folder and allowed extensions
UPLOAD_FOLDER = 'user_data/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Begin the help session
@app.route('/begin', methods=['POST'])
def begin_help():
    user_id = request.form.get('user_id')
    task = request.form.get('task')
    if user_id is None:
        return jsonify({'error': 'No user_id provided'}), 400
    if task is None:
        return jsonify({'error': 'No task provided'}), 400
    gpt.begin_help(user_id, task)
    return jsonify({'message': 'Help session started for user ' + user_id}), 200

# Add the next image
@app.route('/image', methods=['POST'])
def add_image():
    message = None
    if 'message' in request.form:
        message = request.form['message']

    if 'user_id' not in request.form:
        return jsonify({'error': 'No user_id provided'}), 400
    user_id = request.form['user_id']

    if 'photo' not in request.files:
        return jsonify({'error': 'No photo part'}), 400
   
    photo = request.files['photo']
    if photo.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if photo and allowed_file(photo.filename):
        # Save photo to in-memory file
        mem_file = BytesIO()
        photo.save(mem_file)
        mem_file.seek(0)
        base64_image = base64.b64encode(mem_file.read()).decode('utf-8')

        # Pass image to gpt.py
        response = gpt.add_image(user_id, base64_image)

        # # Make sure response is in the correct format
        if "briefExplanation" not in response and "nextAction" not in response:
            return jsonify({'error': 'Invalid response from GPT-4'}), 500
        next_action = response["nextAction"]
        if 'action' not in next_action:
            return jsonify({'error': 'Invalid response from GPT-4'}), 500
        
        # Call the Cloud Vision API
        if next_action['action'] == 'click':
            print("Sending to Cloud Vision!")
            
            # Reset the file pointer to the beginning of the file
            photo.seek(0)
            binary_image = photo.read()

            vision.detect_text_location(binary_image, next_action['text'])

        return response, 200
        
    else:
        return jsonify({'error': 'File type not allowed'}), 400

# Add the next message
@app.route('/message', methods=['POST'])
def add_message():
    if 'user_id' not in request.form:
        return jsonify({'error': 'No user_id provided'}), 400
    user_id = request.form['user_id']

    if 'message' not in request.form:
        return jsonify({'error': 'No message provided'}), 400
    message = request.form['message']

    # Pass message to gpt.py

    return jsonify({'message': 'Message added successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)
