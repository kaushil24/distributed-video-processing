from pathlib import Path
from werkzeug.datastructures import FileStorage


class MediaUtils:
    @staticmethod
    def save_video(video_file: FileStorage, path: Path) -> str:
        video_file.save(path)
        return path
