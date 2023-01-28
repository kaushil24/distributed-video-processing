from flask import Flask, request
from http import HTTPStatus
from flask import Response
import json
from libs.utils import MediaUtils
from decouple import config, Csv
from pathlib import Path
import time
import uuid
import os


app = Flask("load_balancer")

@app.route("/test", methods=['GET', 'POST'])
def test():
    request_dict = request.json
    return Response(json.dumps(request_dict), HTTPStatus.OK, mimetype='application/json')

@app.route("/test2", methods=["POST"])
def test2():
    uploded_file = request.files.get('file')
    request_dict = request.form
    file_name, ext = os.path.splitext(request_dict.get('file_name'))
    file_name = f'{file_name}__{time.strftime("%Y%m%d_%H%M%S")}.{ext}'
    MediaUtils.save_video(uploded_file, Path(f'media/{file_name}'))
    task_id = str(uuid.uuid4())
    response_dict = {'task_id': task_id}
    return Response(json.dumps(response_dict), HTTPStatus.OK, mimetype='application/json')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
