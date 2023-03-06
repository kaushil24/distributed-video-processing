from flask import Flask
from flask import Response
from celery import Celery
from http import HTTPStatus
import zmq
from urllib import parse
from dotenv import load_dotenv
import argparse
import os
import json


app = Flask(__name__)

# app.config["CELERY_BROKER_URL"] = CELERY_BROKER_URL
celery = Celery(app.name)  # , broker=app.config["CELERY_BROKER_URL"])
celery.conf.update(app.config)


@celery.task
def consumer(req_socket_url: str, resp_socket_url: str):
    print("Starting the socket.......")
    context = zmq.Context()
    # recieve work
    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.connect(f"tcp://{req_socket_url}")
    # send work
    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect(f"tcp://{resp_socket_url}")
    print(f"Receiving socket url: {req_socket_url}")
    print(f"Sender socket url: {resp_socket_url}")

    while True:
        print("rec new messageszzzzz")
        jsonData = consumer_receiver.recv_json()
        data = json.loads(jsonData)
        frame_number = data["frame_number"]
        data["frame"]
        data["task_id"]
        print(frame_number)
        # jpg_original = base64.b64decode(data)
        # jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
        # img = cv2.imdecode(jpg_as_np, flags=1)
        # print(img.shape)
        # time.sleep(0.2)
        result = {"data": "done"}
        consumer_sender.send_json(result)


@app.route("/health-check", methods=["GET", "POST"])
def health_check():
    return Response(HTTPStatus.OK)


if __name__ == "__main__":
    argParser = argparse.ArgumentParser()
    # nenv means node-env and senv means shared-env :P
    argParser.add_argument(
        "-task", "--task", help="Start celery or flask?", choices=["celery", "flask"]
    )
    argParser.add_argument("-nenv", "--nenv", help="Pass path to the .env.node[i] file")
    argParser.add_argument("-senv", "--senv", help="Pass path to the shared env file")

    args = argParser.parse_args()

    load_dotenv(args.nenv)
    load_dotenv(args.senv)
    load_dotenv()

    REQ_SOCKET_URL = os.environ.get("REQ_SOCKET_URL")
    RESP_SOCKET_URL = os.environ.get("RESP_SOCKET_URL")
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
    NODE_URL = os.environ.get("NODE_URL")

    app.config["CELERY_BROKER_URL"] = CELERY_BROKER_URL

    consumer.apply_async([REQ_SOCKET_URL, RESP_SOCKET_URL])
    up = parse.urlparse(NODE_URL)
    app.run(debug=True, host=up.hostname, port=up.port)
