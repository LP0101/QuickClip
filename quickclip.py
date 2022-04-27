import os
import string
import random
from ipaddress import ip_network, ip_address
import logging
from venv import create
from time import sleep

from flask import Flask, flash, render_template, request, redirect, send_from_directory, jsonify


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

def check_ip(request):
    ip = ""
    if "X-Real-IP" in request.headers:
        ip = request.headers["X-Real-IP"]
    if "X-Forwarded-For" in request.headers:
        ip = request.headers["X-Forwarded-For"]
    else:
        ip = request.remote_addr
    return ip_address(ip) in ip_network(allowed_upload)

@app.route('/')
def upload_form():
    allowed_upload = check_ip(request)
    return render_template('index.html', allowed_upload=allowed_upload)

@app.route('/upload', methods=['POST'])
def upload_video():
    if not check_ip(request):
        response = {"success": False, "message": "You are not authorized to upload"}
        status_code = 401
    if 'clip' not in request.files:
        response = {"success": False, "message": "'clip' not found in upload"}
        status_code = 400
    file = request.files['clip']
    if file.filename == '':
        response = {"success": False, "message": "empty upload"}
        status_code = 400
    else:
        if not file.mimetype.startswith("video/"):
            response = {"success": False, "message": "File is not a video"}
            status_code = 400
        filename = random_filename(8)
        file.save(os.path.join(library_path, filename))
        response = {"success": True, "clip": filename}
        status_code = 200
        sleep(1)
    return jsonify(response), status_code


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