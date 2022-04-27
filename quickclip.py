import os
import string
import random
from ipaddress import ip_network, ip_address
import logging
from venv import create

from flask import Flask, flash, render_template, request, redirect, send_from_directory


library_path = os.getenv("QUICKCLIP_LIBRARY_PATH")
allowed_upload = os.getenv("QUICKCLIP_ALLOWED_UPLOAD", "0.0.0.0/0")

logger = logging.getLogger()

def check_variables():
    if not library_path:
        logger.critical('Library path not set!\nSet `QUICKCLIP_LIBRARY_PATH`.')
        exit(1)
    if allowed_upload == "0.0.0.0/0":
        logger.warning("`QUICKCLIP_ALLOWED_UPLOAD` not set. Anyone can upload video files.")

def create_app():
    app = Flask(__name__)
    check_variables()
    return app

app = create_app()
logger = logging.getLogger()
app.secret_key = os.urandom(24)

def random_filename(length):
    str = string.ascii_lowercase
    return ''.join(random.choice(str) for i in range(length))

@app.route('/')
def upload_form():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_video():
    ip = ""
    if "X-Real-IP" in request.headers:
        ip = request.headers["X-Real-IP"]
    if "X-Forwarded-For" in request.headers:
        ip = request.headers["X-Forwarded-For"]
    else:
        ip = request.remote_addr
    if ip_address(ip) not in ip_network(allowed_upload):
        flash("You are not authorized to upload")
        return redirect("/")
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
        file.save(os.path.join(library_path, filename))
        return redirect(f"/v/{filename}")

@app.route('/files/<path:filename>')
def custom_static(filename):
    full_path = os.path.join(library_path, filename)

    if os.path.isfile(full_path):
        return send_from_directory(library_path, filename)
    else:
        return "File not found", 404

@app.route('/v/<path:filename>')
def display_video(filename):
    return render_template('clip.html', filename=f"/files/{filename}")