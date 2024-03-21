from flask import Flask, jsonify, request, render_template, Request
import requests as http
from dotenv import load_dotenv
import os

load_dotenv()

KLIPPER_HOST = os.getenv("KLIPPER_HOST")

state = {
    "last_upload_error": False,
    "last_upload_error_cause": ""
}

app = Flask(__name__)

@app.route('/rr_connect', methods=['GET'])
def connect():
    # password
    # time
    # session key
    return jsonify({
        "err": 0,
        "sessionTimeout": 8000,
        "boardType": "duetwifi102",
        "sessionKey": 123456
    })

@app.route('/rr_disconnect', methods=['GET'])
def disconnect():
    return jsonify({
        "err": 0
    })

@app.route('/rr_gcode', methods=['GET'])
def gcode():
    # gcode
    return jsonify({
        "buff": 0
    })

@app.route('/rr_reply', methods=['GET'])
def reply():
    return "this is a reply"

@app.route('/rr_upload', methods=['GET'])
def get_upload():
    if state['last_upload_error']:
        return jsonify({ "err": 1, "cause": state['last_upload_error_cause'] })
    else:
        return jsonify({ "err": 0 })

@app.route('/rr_upload', methods=['POST'])
def post_upload():
    name = request.form.get('name')
    if not name:
        return jsonify({ "err": 1, "cause": "No name provided" })
    
    file = request.form.get('file')
    print(file)
    if 'file' not in request.files:
        return jsonify({ "err": 1, "cause": "No file provided" })
    file = request.files['file']
    
    target_url = f"http://{KLIPPER_HOST}/server/files/upload?path={name}"
    files = {
        'file': (name, file.stream, file.content_type)
    }
    
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
    # dir
    # first
    return jsonify({
        "dir": dir,
        "first": 0,
        "files": [
            {
                "type": "f", # d or f
                "name": "file",
                "size": 10, # 0 if dir
                "date": "2020-01-01 00:00:00"
            },
        ],
        "next": 1,
        "err": 0
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

@app.route('/rr_model', methods=['GET'])
def model():
    # key
    # flags
    return jsonify({
        "key": "key",
        "flags": 0,
        "result": {

        }
    })

@app.route('/rr_move', methods=['GET'])
def move():
    # old
    # new
    # deleteexisting
    return jsonify({
        "err": 0
    })

@app.route('/rr_mkdir', methods=['GET'])
def mkdir():
    # dir
    return jsonify({
        "err": 0
    })

@app.route('/rr_fileinfo', methods=['GET'])
def rename():
    # name
    return jsonify({
        "err": 0,
        "size": 0,
        "lastModified": "2020-01-01 00:00:00",
        "height": 0,
        "layerHeight": 0,
        "printTime": 0,
        "simulatedTime": 0,
        "filament": 0,
        "printDuration": 0,
        "fileName": 0,
        "generatedBy": 0,
    })

if __name__ == '__main__':
    app.run()
