import os
import string
import random
from ipaddress import ip_network, ip_address
import logging
from glob import glob
import subprocess
import threading
from multiprocessing import Manager

from flask import Flask, flash, render_template, request, redirect, send_from_directory, jsonify, send_file


library_path = os.getenv("QUICKCLIP_LIBRARY_PATH")
allowed_upload = os.getenv("QUICKCLIP_ALLOWED_UPLOAD", "0.0.0.0/0")
encode_upload = os.getenv("QUICKCLIP_ENCODE_VIDEOS", 'false') in ('true', '1', 't')
encode_path = os.getenv("QUICKCLIP_ENCODE_PATH", os.path.join(library_path, "enc"))
use_nvenc = os.getenv("QUICKCLIP_ENCODE_VIDEOS_NVENC", 'false') in ('true', 1, 't')

logger = logging.getLogger()

threads = Manager().list()

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

def encode(filename, encode_path, clips_path, nvidia=False):
    print(threads)
    final_file = os.path.join(clips_path, filename)
    unencoded_file = os.path.join(encode_path, filename)
    video_format = "h264_nvenc" if nvidia else "h264"

    ffmpeg_command = f"ffmpeg -i {unencoded_file} -vsync passthrough -movflags faststart -c:v {video_format} -c:a aac -preset default -b:v 10000k {final_file}"


    subprocess.run(ffmpeg_command, shell=True)

    os.remove(unencoded_file)
    threads.remove(filename.split(".")[0])

def encoding(filename):
    return filename in threads


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
        extension = file.filename.split(".")[-1]
        filename_no_ext = random_filename(8)
        filename = filename_no_ext+"."+extension
        if encode_upload:
            file.save(os.path.join(encode_path, filename))
            threads.append(filename_no_ext)
            enc_job = threading.Thread(target=encode, args=(filename, encode_path, library_path), kwargs={"nvidia": True})
            enc_job.start()
        else:
            file.save(os.path.join(library_path, filename))
        response = {"success": True, "clip": filename.split(".")[0]}
        status_code = 200
    return jsonify(response), status_code


@app.route('/files/<path:filename>')
def custom_static(filename):
    if encoding(filename):
        return "Processing", 420
    try:
        full_path = glob(os.path.join(library_path, filename)+"*")[0]
    except Exception as e:
        return "File not found", 404
    if os.path.isfile(full_path):
        return send_file(full_path, cache_timeout=0)
    else:
        return "File not found", 404

@app.route('/status/<path:filename>')
def get_status(filename):
    if encoding(filename):
        return "Processing", 420
    return "Done", 200


@app.route('/v/<path:filename>')
def display_video(filename):
    return render_template('clip.html', filename=f"{filename}")