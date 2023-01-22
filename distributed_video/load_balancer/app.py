from flask import Flask, request
from http import HTTPStatus
from flask import Response
import json
from flask_socketio import SocketIO, send, emit


app = Flask("load_balancer")
socketio = SocketIO(app)

@app.route("/test", methods=['GET', 'POST'])
def index():
    request_dict = request.json
    return Response(json.dumps(request_dict), HTTPStatus.OK, mimetype='application/json')

@app.route("/video-upload", methods=["POST"])
def forward():
    request_dict = request.json
    frame_transfer(request_dict)
    return Response('Received the event')

@socketio.on('frame_transfer')
def frame_transfer(request_dict):
    send(request_dict, namespace='/frame-transfer', to=1)

# def ack():
#     print('Received message confirmation from the node :)')

if __name__ == '__main__':
    socketio.run(app, port=5000)
