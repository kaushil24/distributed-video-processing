from flask import Flask, request
from flask import Response
import time
import os
from distributed_video.libs.utils import MediaUtils
import uuid
from pathlib import Path

app = Flask("load_balancer")


@app.route("/apply-filter", methods=["POST", "GET"])
def apply_filter():
    """
    files = {'file': open(video_path, 'rb')}
    response = requests.post(f"{base_url}/apply-filter", files=files, data={'file_name': file_name})
    """
    uploded_file = request.files.get("file")
    request_dict = request.form
    file_name, ext = os.path.splitext(request_dict.get("file_name"))
    file_name = f'{file_name}__{time.strftime("%Y%m%d_%H%M%S")}{ext}'
    MediaUtils.save_video(uploded_file, Path(f"media/{file_name}"))
    # these are celery tasks
    # lb = LoadBalancer(video_path=video_path)
    # lb.distribute_video()
    # lb.aggregate()
    task_id = str(uuid.uuid4())
    response_dict = {"task_id": task_id}
    return Response(response_dict)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
