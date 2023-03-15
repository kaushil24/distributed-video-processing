import requests
from flask import Flask, request, render_template, Response
import json
from http import HTTPStatus
from distributed_video.db.base import session
from distributed_video.db.models import FrameInfoModel
from sqlalchemy import func
from flask import Flask, jsonify
import os

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
    nodes_listinStr = os.getenv("NODES_ID")
    nodes_list = nodes_listinStr.split(", ")
    result = {
        "nodes_list": nodes_list,
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
    return {"coordinates": str(coordinatesData)}, 200


@app.route("/total-task-time/<string:task_id>")
def get_total_time(task_id):
    total_time = (
        session.query(func.sum(FrameInfoModel.process_time))
        .filter(FrameInfoModel.task == task_id)
        .scalar()
    )

    result = {"total_task_time_in_seconds": total_time, "task_id": task_id}

    print(jsonify(result))
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)
