import os
import string
import random
from unittest.util import _MAX_LENGTH
import magic

from flask import Flask, flash, render_template, request, redirect, send_from_directory
# please note the import from `flask_uploads` - not `flask_reuploaded`!!
# this is done on purpose to stay compatible with `Flask-Uploads`

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["UPLOAD_FOLDER"] = os.getenv("QUICKCLIP_LIBRARY_PATH")

def random_filename(length):
    str = string.ascii_lowercase
    return ''.join(random.choice(str) for i in range(length))

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_video():
    if 'clip' not in request.files:
        flash('No video uploaded')
        return redirect('/')
    file = request.files['clip']
    if file.filename == '':
        flash('No video selected for uploaded')
        return redirect(request.uri)
    else:
        if not file.mimetype.startswith("video/"):
            flash ("Please upload a video file")
            return redirect('/')
        filename = random_filename(8)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(f"/v/{filename}")

@app.route('/files/<path:filename>')
def custom_static(filename):
    full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.isfile(full_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    else:
        return "File not found", 404

@app.route('/v/<path:filename>')
def display_video(filename):
    return render_template('clip.html', filename=f"/files/{filename}")