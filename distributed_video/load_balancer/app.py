from flask import Flask, request
from http import HTTPStatus
from flask import Response
import json
# from libs.utils import MediaUtils
from decouple import config, Csv
from pathlib import Path
import time
import uuid
import os
import zmq

app = Flask("load_balancer")

@app.route("/test", methods=['GET', 'POST'])
def test():
    request_dict = request.json
    return Response(json.dumps(request_dict), HTTPStatus.OK, mimetype='application/json')

@app.route("/test2", methods=["POST"])
def test2():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://127.0.0.1:5557")

    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.bind("tcp://127.0.0.1:6000")
    dummy = request.json
    # uploded_file = request.files.get('file')
    # request_dict = request.form
    # file_name, ext = os.path.splitext(request_dict.get('file_name'))
    # file_name = f'{file_name}__{time.strftime("%Y%m%d_%H%M%S")}.{ext}'
    # # MediaUtils.save_video(uploded_file, Path(f'media/{file_name}'))
    # task_id = str(uuid.uuid4())
    response_dict = {'task_id': "asndkasnd3242qwsed"}
    tasks = ["task1", "task2", "task3"]
    for task in tasks:
        work_message = { 'task' : task }
        zmq_socket.send_json(work_message)
    while len(tasks) is not 0:
        print("done Sending")    
        work = consumer_receiver.recv_json()
        data = work['data']
        print(data)
        tasks.remove(data)

    return Response(json.dumps(response_dict), HTTPStatus.OK, mimetype='application/json')

@app.route("/get-triangles", methods=["POST"])
def get_triangles():
    """
    video = request.form.video
    videl_dir = video.save()

    distribute_frame(video_dir)  # celery task

    return Response({"tracking_id": sdsd})
    """
    pass

if __name__ == '__main__':
    app.run(port=5000, debug=True)
