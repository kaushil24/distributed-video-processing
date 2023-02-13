from flask import Flask, request
from http import HTTPStatus
from flask import Response
import json
import zmq
import re
import base64
import json
import cv2

app = Flask("load_balancer")


@app.route("/test", methods=["GET", "POST"])
def test():
    request_dict = request.json
    return Response(
        json.dumps(request_dict), HTTPStatus.OK, mimetype="application/json"
    )


@app.route("/test2", methods=["POST"])
def test2():
    context = zmq.Context()
    zmq_socket = context.socket(zmq.PUSH)
    zmq_socket.bind("tcp://127.0.0.1:5557")

    consumer_receiver = context.socket(zmq.PULL)
    consumer_receiver.bind("tcp://127.0.0.1:6000")

    data = request.json
    fileName = data["fileName"]
    fileNameWithPath = "./../inputDump/" + data["fileName"] + ".mp4"
    byteString = re.sub("^.*,", "", data["video"])
    videoData = base64.b64decode(byteString)
    with open(fileNameWithPath, "wb") as out_file:  # open for [w]riting as [b]inary
        out_file.write(videoData)
    # print(fileName)
    # cmd = "ffprobe -v quiet -print_format json -show_streams"
    # args = shlex.split(cmd)
    # args.append(fileName)
    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
    # ffprobeOutput = subprocess.check_output(args).decode('utf-8')
    # ffprobeOutput = json.loads(ffprobeOutput)
    # frameCount = ffprobeOutput['streams'][0]['nb_frames']
    cam = cv2.VideoCapture(fileNameWithPath)

    currentframe = 0
    tasks = []

    while True:
        # reading from frame
        ret, frame = cam.read()

        if ret:
            # if video is still left continue creating images
            name = "./../imageDump/" + fileName + "_" + str(currentframe) + ".jpg"

            # writing the extracted images
            cv2.imwrite(name, frame)
            tasks.append(fileName + "_" + str(currentframe))
            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam.release()
    cv2.destroyAllWindows()

    response_dict = {"task_id": "asndkasnd3242qwsed"}
    for task in tasks:
        work_message = {"task": task}
        zmq_socket.send_json(work_message)
    while len(tasks) is not 0:
        print("done Sending")
        work = consumer_receiver.recv_json()
        data = work["data"]
        print(data)
        tasks.remove(data)

    return Response(
        json.dumps(response_dict), HTTPStatus.OK, mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(port=5000, debug=True)
