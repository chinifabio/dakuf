from flask import Flask, jsonify, request
import requests as http, re

from klipper_model import *
from duet_model import *

KLIPPER_HOST = "localhost:7125"

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024

@app.route('/rr_gcode', methods=['GET'])
def gcode():
    """
    Run a gcode command on the printer
    If the gcode is a M32 command, it will be sent to the Klipper API to start a print
    If the gcode is any other command, it will be sent to the Klipper API to run as a script
    """
    gcode = request.args.get('gcode')
    if not gcode:
        return jsonify({
            "buff": 1000
        })

    start_print_re = re.compile(r'M32\s+\"?([\w. \-/]+)\"?')
    match = start_print_re.match(gcode)
    if match:
        target_url = f"http://{KLIPPER_HOST}/printer/print/start?filename={match.group(1)}"
    else:
        target_url = f"http://{KLIPPER_HOST}/printer/gcode/script?script={gcode}"

    response = http.post(target_url)
    if response.status_code == 200:
        return jsonify({
            "buff": 1000
        })
    else:
        return jsonify({
            "err": 1,
            "cause": response.text
        })

@app.route('/rr_upload', methods=['POST'])
def upload():
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
        return jsonify({ "err": 0 })
    else:
        return jsonify({ "err": 1, "cause": "Error uploading file" })

def is_valid_root(root):
    target_url = f"http://{KLIPPER_HOST}/server/files/roots"
    response = http.get(target_url)
    if response.status_code == 200:
        roots = [x['name'] for x in response.json()['result']]
        return root in roots
    else:
        return False

@app.route('/rr_filelist', methods=['GET'])
def filelist():
    dir = request.args.get('dir')
    if not dir:
        dir = 'gcodes'
    dir = re.sub(r'\d+:', '', dir)
    dir = re.sub(r'/$', '', dir)
    dir = re.sub(r'^/', '', dir)

    root = dir.split('/')[0]
    if not is_valid_root(root):
        return jsonify({
            "err": 2,
            "cause": "Root directory does not exist"
        })
    
    target_url = f"http://{KLIPPER_HOST}/server/files/list?root={root}"
    response = http.get(target_url)
    if response.status_code == 200:
        klipper_files = KlipperFileList(**response.json())
        duet_files = DuetFileList.from_klipper_tree(klipper_files.generate_tree(), dir=dir)
        return jsonify(duet_files.__dict__)
    else:
        return jsonify({
            "err": 1,
            "cause": response.text
        })

@app.route('/rr_status', methods=['GET'])
def status():
    """
    Get the status of the printer
    ----------------
    'P' -> Printing
    'I' -> Idle
    'A' -> Paused
    ----------------
    """
    target_url = f"http://{KLIPPER_HOST}/printer/objects/query?print_stats"
    response = http.get(target_url)
    if response.status_code == 200:
        data = response.json()
        status_map = {
            "standby": "I",
            "printing": "P",
            "paused": "A"
        }
        status = status_map.get(data['result']['status']['print_stats']['state'], "?")
        return jsonify({ "status": status })
    else:
        return jsonify({ "status": "x" })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)