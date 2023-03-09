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
import numpy as np
import cv2
from distributed_video.video_processor.dlib_distributed import dlib_main
import time

from distributed_video.db.base import session
from distributed_video.db.models import FrameInfoModel


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
        jsonData = consumer_receiver.recv().decode()
        # print(jsonData)
        # Deserialize the JSON-encoded string
        data = json.loads(jsonData)

        # Convert the hex-encoded image data back into a byte string
        image_hex = data["image"]
        image_bytes = bytes.fromhex(image_hex)

        # Decode the image from the byte string
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        startTime = time.time()
        dlib_main(image, data["frame_number"], data["task_id"])
        endTime = time.time()
        processTime = endTime - startTime
        mdl = FrameInfoModel(
            task=data["task_id"],
            frame_number=data["frame_number"],
            coordinates={"hello": "world"},
            process_time=processTime,
            node=app.config.get("NODE_ID"),
        )
        mdl.save()
        session.commit()
        # data = json.loads(jsonData)
        # frame_number = data["frame_number"]
        # print(frame_number)
        # img_data = data["frame"]
        # data["task_id"]
        # img_data = bytes.fromhex(img_data)
        # img_np = cv2.imdecode(np.fromstring(img_data, dtype=np.uint8))
        # print(img_np.shape)
        # time.sleep(0.2)
        result = {"data": "done"}
        consumer_sender.send_json(result)

        # to commit to the db
        # mdl = FrameInfoModel(task="hex0", frame_number=1, coordinates={'a':'b'}, process_time=2, node=app.config.get("NODE_ID"))
        # mdl.save()
        # session.commit()


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
    NODE_ID = os.environ.get("NODE_ID")

    app.config["CELERY_BROKER_URL"] = CELERY_BROKER_URL
    app.config["NODE_ID"] = NODE_ID

    consumer.apply_async([REQ_SOCKET_URL, RESP_SOCKET_URL])
    up = parse.urlparse(NODE_URL)
    app.run(debug=True, host=up.hostname, port=up.port)
