from distributed_video.load_balancer.node_manager import NodesDirectory
from distributed_video.load_balancer.celery_worker import celery_app
import cv2
import json
import zmq
from distributed_video.load_balancer.aggregator import aggregator
from distributed_video.load_balancer.constants import RESP_SOCKET_URL


# Deprecated. Use bare functions instead
# Not used anywhere!!!!!
class LoadBalancer:
    def send_frame(self, frameData):
        # print(frame)
        # frameData = {
        #     "task_id": self.task_id,
        #     'frame': frame,
        #     "frame_number": frameNumber,
        # }

        jsonFrameData = json.dumps(frameData)

        self.nodes_directory.send_data_as_string(jsonFrameData)

    def dissect_video(self):
        fileNameWithPath = "media/" + self.file_name
        cam = cv2.VideoCapture(fileNameWithPath)
        print(fileNameWithPath)
        currentframe = 0
        success, frame = cam.read()
        print("here")
        print(success)
        # Loop through the video frames
        cap = cv2.VideoCapture(fileNameWithPath)
        cap.get(cv2.CAP_PROP_FPS)
        while True:
            ret, frame = cam.read()
            if ret:
                # Save the frame as an image
                image_bytes = cv2.imencode(".jpg", frame)[1].tobytes()
                image_hex = image_bytes.hex()
                frameData = {
                    "image": image_hex,
                    "frame_number": currentframe,
                    "task_id": self.task_id,
                }
                print(currentframe)
                self.send_frame(frameData=frameData)
                currentframe += 1
            else:
                break
        # while success:
        #     image_bytes = cv2.imencode(".jpg", frame)[1].tobytes()

        #     image_hex = image_bytes.hex()

        #     currentframe += 1
        #     # Process the frame bytes here
        #     frameData = {"image": image_hex, "frame_number": currentframe, "task_id": self.task_id}
        #     print(currentframe)
        #     self.send_frame(frameData=frameData)
        #     # Read the next frame
        #     # success, frame = cam.read()

        # Release the video file
        cam.release()
        cv2.destroyAllWindows()

    def distribute_video(self):
        self.dissect_video()

    def __init__(
        self, file_name: str, task_id: str, nodes_directory: NodesDirectory
    ) -> None:
        self.task_id = task_id
        self.file_name = file_name
        self.nodes_directory = nodes_directory


def send_frame(frameData: dict, nodes_director: NodesDirectory):
    jsonFrameData = json.dumps(frameData)
    nodes_director.send_data_as_string(jsonFrameData)


@celery_app.task(bind=True)
def dissect_video(self, file_name: str):
    task_id = self.request.id
    # task_id = 't7'
    print(type(file_name))
    fileNameWithPath = "media/" + file_name
    cam = cv2.VideoCapture(fileNameWithPath)
    print(fileNameWithPath)
    currentframe = 0
    processed_frames = 0
    success, frame = cam.read()
    print("here")
    print(success)
    nd = NodesDirectory()
    nd.close_all_sockets()
    nd.bind_all_sockets()

    print("Starting the socket.......")
    context1 = zmq.Context()

    # send work
    ack_socket = context1.socket(zmq.PULL)
    print("----------------------", RESP_SOCKET_URL)
    ack_socket.bind(f"tcp://{RESP_SOCKET_URL}")
    print(f"Listening to socket url: {RESP_SOCKET_URL}")

    # Loop through the video frames
    cap = cv2.VideoCapture(fileNameWithPath)
    cap.get(cv2.CAP_PROP_FPS)
    # @todo: Placeholder
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    while True:
        ret, frame = cam.read()
        if ret:
            # Save the frame as an image
            image_bytes = cv2.imencode(".jpg", frame)[1].tobytes()
            image_hex = image_bytes.hex()
            frameData = {
                "image": image_hex,
                "frame_number": currentframe,
                "task_id": task_id,
            }
            print(currentframe)
            send_frame(frameData, nd)
            currentframe += 1
            self.update_state(
                state="STARTED",
                meta={
                    "sent_frames": currentframe,
                    "total_frames": total_frames,
                    "processed_frames": processed_frames,
                },
            )
            # if currentframe == 5:
            #     nd.publish_EOF()
            #     nd.close_all_sockets()
            #     break
            # time.sleep(2)
        else:
            nd.publish_EOF()
            nd.close_all_sockets()
            break
    cam.release()
    cv2.destroyAllWindows()

    # @todo: Add aggregator logic
    # Read from the response queue for EOF from all the nodes
    len(nd.nodes)
    # psuedo code:
    # create a consumer socket that will read from RESP_SOCKEK_URL
    # keep reading on this socket until you get an EOF from all the nodes
    # once you have that, call the aggregator
    # after aggregator, change the status of the task to completed

    # def receive_eof(nodes_id: int, resp_socket_url: str, nd: NodesDirectory):
    # Load total nodes created and create node-status dict with default status "pending"
    node_status = {node.id: "pending" for node in nd.nodes}

    while True:
        # Receive the EOF message
        message = ack_socket.recv_string()
        data = json.loads(message)
        print(data)
        # If EOF received, mark "done" in node-status dict
        if data.get("EOF"):
            node_status[data["node"]] = "done"
        else:
            # else calculate the number of nodes processed
            processed_frames += 1
            self.update_state(
                state="STARTED",
                meta={
                    "sent_frames": currentframe,
                    "total_frames": total_frames,
                    "processed_frames": processed_frames,
                },
            )
        # If all done, then call aggregator function
        if "pending" not in node_status.values():
            break

    _ = aggregator(task_id=task_id, total_frames=processed_frames)
    self.update_state(
        state="COMPLETED",
        meta={
            "sent_frames": currentframe,
            "total_frames": total_frames,
            "processed_frames": processed_frames,
        },
    )
    # return "SUCCESS"
