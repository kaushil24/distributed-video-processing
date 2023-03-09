from distributed_video.load_balancer.node_manager import NodesDirectory
import cv2
import json


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
