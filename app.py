from flask import Flask, jsonify, request, render_template, Request
import requests as http
from dotenv import load_dotenv
import os

from klipper_model import *
from duet_model import *

load_dotenv()

KLIPPER_HOST = os.getenv("KLIPPER_HOST")

state = {
    "last_upload_error": False,
    "last_upload_error_cause": ""
}

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

@app.route('/rr_gcode', methods=['GET'])
def gcode():
    # gcode
    return jsonify({
        "buff": 0
    })

@app.route('/rr_upload', methods=['GET'])
def get_upload():
    if state['last_upload_error']:
        return jsonify({ "err": 1, "cause": state['last_upload_error_cause'] })
    else:
        return jsonify({ "err": 0 })

@app.route('/rr_upload', methods=['POST'])
def post_upload():
    """
    Upload a file to the printer

    The duet expects a POST request with a file as the body and the name of the file as a query parameter.
    Klipper expects a multipart/form-data request with the file as the 'file' field.
    """
    name = request.args.get('name')
    if not name:
        return jsonify({ "err": 1, "cause": "No name provided" })
    name = name.split('/')[-1]

    target_url = f"http://{KLIPPER_HOST}/server/files/upload?path={name}"
    files = { 'file': (name, request.stream, 'application/octet-stream') }
    response = http.post(target_url, files=files)

    if response.status_code in [200, 201]:
        state['last_upload_error'] = False
        state['last_upload_error_cause'] = ''
        return jsonify({ "err": 0 })
    else:
        state['last_upload_error'] = True
        state['last_upload_error_cause'] = response.text
        return jsonify({ "err": 1, "cause": "Error uploading file" })

@app.route('/rr_download', methods=['GET'])
def download():
    # name
    return "this is the file content" # 404 otherwise

@app.route('/rr_delete', methods=['GET'])
def delete():
    # name
    # recursive
    return jsonify({
        "err": 0
    })

@app.route('/rr_filelist', methods=['GET'])
def filelist():
    dir = request.args.get('dir')
    if not dir:
        dir = 'gcodes'
    target_url = f"http://{KLIPPER_HOST}/server/files/list?root={dir}"
    
    response = http.get(target_url)
    if response.status_code == 200:
        print(response.json())
        klipper_files = KlipperFileList(**response.json())
        duet_files = DuetFileList.from_klipper_file_list(klipper_file_list=klipper_files, dir=dir)
        return jsonify(duet_files.__dict__)
    else:
        return jsonify({
            "err": 1,
            "cause": response.text
        })

@app.route('/rr_files', methods=['GET'])
def files():
    # dir
    # first
    # flagDirs
    return jsonify({
        "dir": "dir",
        "first": 0,
        "files": [
            "file1",
            "file2",
        ],
        "next": 0,
        "err": 0
    })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
