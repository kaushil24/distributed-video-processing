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
    uploded_file = request.files.get("file")
    request_dict = request.form
    file_name, ext = os.path.splitext(request_dict.get("file_name"))
    file_name = f"{file_name}__{task_id}{ext}"
    MediaUtils.save_video(uploded_file, Path(f"media/{file_name}"))
    lb = LoadBalancer(file_name=file_name, task_id=task_id, nodes_directory=nd)
    lb.distribute_video()
    # lb.aggregate()
    response_dict = {"task_id": task_id, "message": "uploaded successfully"}
    # return Response(response_dict)

    nd.close_all_sockets()
    return Response(
        json.dumps(response_dict), HTTPStatus.OK, mimetype="application/json"
    )


if __name__ == "__main__":
    app.run(port=6000, debug=True)
