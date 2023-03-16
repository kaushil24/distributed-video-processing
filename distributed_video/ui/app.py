import requests
from flask import Flask, request, render_template, Response, send_file
import json
from http import HTTPStatus
from distributed_video.db.base import session
from distributed_video.db.models import FrameInfoModel
from sqlalchemy import func
from flask import Flask, jsonify
import os
from decouple import config, Csv
from typing import List


app = Flask(__name__)

nodesList = []


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html",
    )


@app.route("/", methods=["POST"])
def sendData():
    data = request.json
    req_dict = {"file": data["file"], "filename": data["filename"]}
    response = requests.post("http://localhost:6000/apply-filter", data=req_dict)
    return Response(
        json.dumps(response.json()), HTTPStatus.OK, mimetype="application/json"
    )


@app.route("/node-stats/<int:node_id>/<string:task_id>")
def get_node_stats(node_id, task_id):
    avg_time_per_node = (
        session.query(func.avg(FrameInfoModel.process_time))
        .filter(FrameInfoModel.node == node_id, FrameInfoModel.task == task_id)
        .scalar()
    )

    result = {"node_id": node_id, "avg_time_per_frame": avg_time_per_node}

    print(jsonify(result))
    return jsonify(result), 200


@app.route("/nodes-list")
def get_nodesList():
    nodes_listinStr = config("NODES_ID", cast=Csv())
    nodes_list_ip = config("NODES", cast=Csv())

    result = {
        "nodes_list": nodes_list_ip,
        "nodes_ip": nodes_list_ip,
        "health": ["OK" for _ in range(len(nodes_list_ip))],
    }

    return jsonify(result), 200


@app.route("/coordinates-frame/<string:task_id>/<int:frame_number>")
def getcoordinatesofFrame(task_id, frame_number):
    coordinatesData = (
        session.query(FrameInfoModel.coordinates)
        .filter(
            FrameInfoModel.frame_number == frame_number, FrameInfoModel.task == task_id
        )
        .first()
    )
    # coordinates = json.dumps(coordinatesData, cls=AlchemyEncoder)
    # result = {

    #     'coordinates': coordinates,
    # }
    result = ""
    for data in coordinatesData:
        result = result + str(data)
    return {"coordinates": result}, 200


@app.route("/task-stats/<string:task_id>")
def task_stats(task_id):
    total_time = (
        session.query(func.sum(FrameInfoModel.process_time))
        .filter(FrameInfoModel.task == task_id)
        .scalar()
    )
    total_frames = (
        session.query(func.count(FrameInfoModel.frame_number))
        .filter(FrameInfoModel.task == task_id)
        .scalar()
    )

    frames_per_node = (
        session.query(FrameInfoModel.node, func.count(FrameInfoModel.frame_number))
        .filter(FrameInfoModel.task == task_id)
        .group_by(FrameInfoModel.node)
        .all()
    )
    result = {
        "total_task_time_in_seconds": total_time,
        "task_id": task_id,
        "frames_processed": total_frames,
        "frames_per_node": str(frames_per_node),
    }

    print(jsonify(result))
    return jsonify(result), 200


@app.route("/tasksInfoFromCelery/<string:task>")
def getTaskInfo(task):
    response = requests.get("http://localhost:6000/tasks/" + task)
    return Response(
        json.dumps(response.json()), HTTPStatus.OK, mimetype="application/json"
    )


@app.route("/get-stats-node/<task>", methods=["GET"])
def get_stats(task: str):
    # @todo: Add logic to return different statistics
    model_query: List[FrameInfoModel] = FrameInfoModel.query().filter_by(task=task)
    response = []
    for frame_info in model_query:
        response.append({"task": frame_info.process_time})

    # @todo: How to use flask's Response?
    return jsonify(response)


@app.route("/check-video/<taskid>", methods=["GET"])
def check_video(taskid):
    # Construct the full path to the file
    path = os.path.join("../load_balancer/media", taskid + ".avi")
    if os.path.isfile(path):
        return jsonify({"status": "success", "message": "File exists"})
    else:
        return jsonify({"status": "error", "message": "File not found"})


@app.route("/video/<taskid>", methods=["GET"])
def get_video(taskid):
    path = "../load_balancer/media/" + taskid + ".avi"
    # Replace 'path/to/video.mp4' with the actual path to your video file
    return send_file(path, mimetype="video/avi")


if __name__ == "__main__":
    app.run(debug=True)
