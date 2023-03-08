from distributed_video.load_balancer.node_manager import NodesDirectory
import cv2
import json


class LoadBalancer:
    def send_frame(self, frameData, frameNumber):
        # print(frame)
        # frameData = {
        #     "task_id": self.task_id,
        #     'frame': frame,
        #     "frame_number": frameNumber,
        # }

        print("here")
        jsonFrameData = json.dumps(frameData)
        print(
            [
                self.nodes_directory.nodes[i].req_socket_url
                for i in range(len(self.nodes_directory.nodes))
            ]
        )
        self.nodes_directory.send_default(jsonFrameData)

    def dissect_video(self):
        fileNameWithPath = "media/" + self.file_name
        cam = cv2.VideoCapture(fileNameWithPath)
        print(fileNameWithPath)
        currentframe = 0
        success, frame = cam.read()
        print("here")
        print(success)
        # Loop through the video frames
        while success:
            image_bytes = cv2.imencode(".jpg", frame)[1].tobytes()

            # Convert the image bytes to a hex-encoded string
            image_hex = image_bytes.hex()

            # # Create a dictionary containing the image data
            # data = {'image': image_hex}

            # # Serialize the dictionary as a JSON-encoded string
            # json_data = json.dumps(data)

            # # Send the JSON-encoded string over the socket
            # socket.send(json_data.encode())

            currentframe += 1
            # Process the frame bytes here
            frameData = {"image": image_hex}
            self.send_frame(frameData=frameData, frameNumber=currentframe)
            # Read the next frame
            # success, frame = cam.read()

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
