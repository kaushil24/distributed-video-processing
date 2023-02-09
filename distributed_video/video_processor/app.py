# from flask import Flask, request
# from http import HTTPStatus
# from flask import Response
# import json
# from flask import Flask, request
# from http import HTTPStatus
# from flask import Response
# import json
import zmq
import time
# from flask_socketio import SocketIO, send

# app = Flask("video_processor")

# @app.route("/upload-video", methods=['POST'])
# def index():
#     request_dict = request.json
#     return Response(json.dumps(request_dict), HTTPStatus.OK)

# @socketio.on('frame_transfer', namespace='/frame-transfer')
# def frame_transfer(message_json):
#     print(f'received message: {message_json}')
#     send({'status': 'Message received successfully'}, json=True)

def consumer():
    # consumer_id = random.randrange(1,10005)
    # print "I am consumer #%s" % (consumer_id)
    context = zmq.Context()
    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect("tcp://127.0.0.1:5557")
    # send work
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect("tcp://127.0.0.1:5558")
    
    while True:
        work = consumer_receiver.recv_json()
        data = work['task']
        time.sleep(1)
        print(data)
        result = { 'data' : data}
        consumer_sender.send_json(result)


consumer()


# if __name__ == '__main__':
#     app.run(port=80085, debug=True)
