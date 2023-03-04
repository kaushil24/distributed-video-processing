from flask import Flask
from flask import Response
from celery import Celery
from http import HTTPStatus
import zmq
import time
from urllib import parse


# @todo: Since we're starting only one node here, the variables are hard-coded
# once I have the start-node.sh configured, it should read from env-vars.
# Refer start-node.sh for more info
REQ_SOCKET_URL = "127.0.0.1:9008"  # {os.environ.get('REQ_SOCKET_URL')}
RESP_SOCKET_URL = "127.0.0.1:9069"  # {os.environ.get('RESP_SOCKET_URL')}
RABBIT_MQ_URL = "amqp://localhost:5679"
NODE_URL = "http://0.0.0.0:5001"

app = Flask(__name__)
app.config["CELERY_BROKER_URL"] = RABBIT_MQ_URL
celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)


@celery.task
def consumer():
    print("Starting the socket.......")
    context = zmq.Context()
    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect(f"tcp://{REQ_SOCKET_URL}")
    # send work
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect(f"tcp://{RESP_SOCKET_URL}")
    print(f"Receiving socket url: {REQ_SOCKET_URL}")
    print(f"Sender socket url: {RESP_SOCKET_URL}")

    while True:
        print("rec new messages")
        work = consumer_receiver.recv_json()
        data = work["task"]
        time.sleep(0.2)
        print(data)
        result = {"data": data}
        consumer_sender.send_json(result)


@app.route("/health-check", methods=["GET", "POST"])
def health_check():
    return Response(HTTPStatus.OK)


if __name__ == "__main__":
    consumer.apply_async()
    up = parse.urlparse(NODE_URL)
    app.run(debug=True, host=up.hostname, port=up.port)
