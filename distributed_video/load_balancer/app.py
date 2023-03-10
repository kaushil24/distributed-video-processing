from flask import Flask, request
from flask import Response
import uuid
import json
from http import HTTPStatus
from distributed_video.load_balancer.load_balancer import dissect_video
from distributed_video.libs.utils import MediaUtils
import os
from pathlib import Path
from distributed_video.db.models import FrameInfoModel
from typing import List
from flask import jsonify
from celery.result import AsyncResult
from celery_worker import celery_app

app = Flask("load_balancer")


@app.route("/apply-filter", methods=["POST", "GET"])
def apply_filter():
    """
    files = {'file': open(video_path, 'rb')}
    response = requests.post(f"{base_url}/apply-filter", files=files, data={'file_name': file_name})
    """
    task_id = str(uuid.uuid4())
    uploded_file = request.files.get("file")
    request_dict = request.form
    file_name, ext = os.path.splitext(request_dict.get("file_name"))
    file_name = f"{file_name}__{task_id}{ext}"
    MediaUtils.save_video(uploded_file, Path(f"media/{file_name}"))
    # lb = LoadBalancer(file_name=file_name, task_id=task_id, nodes_directory=nd)
    # lb.distribute_video()
    # task: AsyncResult = dissect_video.apply_async(kwargs={'file_name': file_name, 'nodes_directory':nd})
    task: AsyncResult = dissect_video.apply_async([file_name])
    # dissect_video(file_name)
    # lb.aggregate()
    response_dict = {"task_id": task.id, "message": "uploaded successfully"}
    # return Response(response_dict)

    return Response(
        json.dumps(response_dict), HTTPStatus.OK, mimetype="application/json"
    )


@app.route("/tasks/<task>", methods=["GET", "POST"])
def test1(task: str):
    print("-------------", task)
    result = AsyncResult(task, app=celery_app)
    print("--------------", result.info)
    return jsonify(result.info)


@app.route("/get-stats/<task>", methods=["GET"])
def get_stats(task: str):
    # @todo: Add logic to return different statistics
    model_query: List[FrameInfoModel] = FrameInfoModel.query().filter_by(task=task)
    response = []
    for frame_info in model_query:
        response.append({"task": frame_info.task})

    # @todo: How to use flask's Response?
    return jsonify(response)


if __name__ == "__main__":
    app.run(port=6000, debug=True)
