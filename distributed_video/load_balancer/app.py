from flask import Flask, request
from flask import Response
import uuid
import re
import base64
import json
from http import HTTPStatus
from load_balancer import LoadBalancer
from distributed_video.load_balancer.node_manager import NodesDirectory


app = Flask("load_balancer")


@app.route("/apply-filter", methods=["POST", "GET"])
def apply_filter():
    """
    files = {'file': open(video_path, 'rb')}
    response = requests.post(f"{base_url}/apply-filter", files=files, data={'file_name': file_name})
    """
    nd = NodesDirectory()
    nd.close_all_sockets()
    nd.bind_all_sockets()

    task_id = str(uuid.uuid4())
    data = request.json
    fileNameWithPath = "./media/" + task_id + ".mp4"
    byteString = re.sub("^.*,", "", data["videoData"])
    videoData = base64.b64decode(byteString)
    with open(fileNameWithPath, "wb") as out_file:  # open for [w]riting as [b]inary
        out_file.write(videoData)
    # these are celery tasks
    print("here")
    lb = LoadBalancer(task_id=task_id, nodes_directory=nd)
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
