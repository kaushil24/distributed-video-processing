from flask import Flask, request
from flask import Response
import uuid
import json
from http import HTTPStatus
from load_balancer import LoadBalancer
from distributed_video.libs.utils import MediaUtils
import os
from distributed_video.load_balancer.node_manager import NodesDirectory
from pathlib import Path
from distributed_video.db.models import FrameInfoModel
from typing import List
from flask import jsonify
import re
import base64


app = Flask("load_balancer")


@app.route("/apply-filter", methods=["POST", "GET"])
def apply_filter():
    """
    files = {'file': open(video_path, 'rb')}
    response = requests.post(f"{base_url}/apply-filter", files=files, data={'file_name': file_name})
    """
    nd = NodesDirectory()
    # nd.close_all_sockets()
    nd.bind_all_sockets()
    task_id = str(uuid.uuid4())
    request_dict = request.form
    byteString = re.sub("^.*,", "", request_dict.get("file"))
    bytes_data = base64.b64decode(byteString)

    file_name, ext = os.path.splitext(request_dict.get("filename"))
    file_name = f"{file_name}__{task_id}{ext}"
    MediaUtils.save_video(bytes_data, Path(f"media/{file_name}"))
    lb = LoadBalancer(file_name=file_name, task_id=task_id, nodes_directory=nd)
    lb.distribute_video()
    # lb.aggregate()
    response_dict = {"task_id": task_id, "message": "uploaded successfully"}
    # return Response(response_dict)

    nd.close_all_sockets()
    return Response(
        json.dumps(response_dict), HTTPStatus.OK, mimetype="application/json"
    )


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
