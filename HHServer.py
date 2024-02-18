from flask import Flask, request, jsonify
#from werkzeug.utils import secure_filename
import os
from io import BytesIO
import base64
import gpt

app = Flask(__name__)

# Configure the upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/begin', methods=['POST'])
def begin_help():
    user_id = request.form.get('user_id')
    if user_id is None:
        return jsonify({'error': 'No user_id provided'}), 400
    os.makedirs(app.config['UPLOAD_FOLDER'] + user_id + '/', exist_ok=True)
    return jsonify({'message': 'Help session started for user ' + user_id}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
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

        # Start the help session by passing into gpt.py
        #gpt.

        #filename = secure_filename(photo.filename)
        #photo.save(os.path.join(app.config['UPLOAD_FOLDER'] + user_id + '/', filename))
        return jsonify({'message': 'Photo uploaded successfully'}), 200
    else:
        return jsonify({'error': 'File type not allowed'}), 400

if __name__ == '__main__':
    app.run(debug=True)
