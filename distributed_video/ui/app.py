import requests
from flask import Flask, request, render_template, Response
import json
from http import HTTPStatus

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(debug=True)
