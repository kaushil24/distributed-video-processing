from flask import Flask, request
from http import HTTPStatus
from flask import Response
import json
from flask import Flask, request
from http import HTTPStatus
from flask import Response
import json
from flask_socketio import SocketIO, send

app = Flask("video_processor")
socketio = SocketIO(app)

@app.route("/test", methods=['GET', 'POST'])
def index():
    request_dict = request.json
    return Response(json.dumps(request_dict), HTTPStatus.OK)

@socketio.on('frame_transfer', namespace='/frame-transfer')
def frame_transfer(message_json):
    print(f'received message: {message_json}')
    send({'status': 'Message received successfully'}, json=True)

if __name__ == '__main__':
    socketio.run(app, port=80085)
