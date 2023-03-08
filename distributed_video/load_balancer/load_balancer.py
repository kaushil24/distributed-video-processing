from distributed_video.load_balancer.node_manager import NodesDirectory
import cv2
import json


class LoadBalancer:
    def send_frame(self, frame, frameNumber):
        # print(frame)
        frameData = {
            "task_id": self.task_id,
            "frame": frame,
            "frame_number": frameNumber,
        }
        print("here")
        jsonFrameData = json.dumps(frameData)
        self.nodes_directory.send_json(jsonFrameData)

    def dissect_video(self):
        fileNameWithPath = "./media/" + self.file_name
        cam = cv2.VideoCapture(fileNameWithPath)

        currentframe = 0
        success, frame = cam.read()

        # Loop through the video frames
        while success:
            # Convert the frame to bytes
            frame_bytes = frame.tobytes().hex()
            # frame_bytes_string = base64.b64encode(frame_bytes).decode()
            # frame_bytes_string = frame_bytes.decode()
            currentframe += 1
            # Process the frame bytes here
            self.send_frame(frame=frame_bytes, frameNumber=currentframe)
            # Read the next frame
            success, frame = cam.read()

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
