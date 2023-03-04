from distributed_video.load_balancer.node_manager import NodesDirectory


class LoadBalancer:
    def __init__(self, video_path: str, nodes_directory: NodesDirectory) -> None:
        self.video_path = video_path
        self.nodes_directory = nodes_directory

    def send_frame(self, frame):
        pass

    def dissect_video(self):
        pass

    def distribute_video(self):
        # should call send_frame and disect_video
        pass
