from flask import Flask, request
from http import HTTPStatus
from flask import Response
import json
from pathlib import Path
import time
import uuid
import os
import zmq
import re
import base64

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

    data = request.json
    byteString = re.sub("^.*,", "", data['video'])
    videoData = base64.b64decode(byteString)
    with open('output.mp4', "wb") as out_file:  # open for [w]riting as [b]inary
        out_file.write(videoData)
    # task_id = str(uuid.uuid4())
    response_dict = {'task_id': "asndkasnd3242qwsed"}
    # tasks = ["task1", "task2", "task3"]
    # for task in tasks:
    #     work_message = { 'task' : task }
    #     zmq_socket.send_json(work_message)
    # while len(tasks) is not 0:
    #     print("done Sending")    
    #     work = consumer_receiver.recv_json()
    #     data = work['data']
    #     print(data)
    #     tasks.remove(data)

    return Response(json.dumps(response_dict), HTTPStatus.OK, mimetype='application/json')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
