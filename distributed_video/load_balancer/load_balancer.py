class LoadBalancer:
    def __init__(self, video_path: str) -> None:
        self.video_path = video_path

    def send_frame(self):
        pass

    def dissect_video(self):
        pass

    def distribute_video(self):
        # should call send_frame and disect_video
        pass
