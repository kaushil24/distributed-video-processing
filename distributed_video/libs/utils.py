from pathlib import Path
from werkzeug.datastructures import FileStorage


class MediaUtils:
    @staticmethod
    def save_video(video_file: FileStorage, abs_path: Path) -> str:
        video_file.save(abs_path)
        return abs_path
