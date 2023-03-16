from pathlib import Path
from decouple import config
import os

# @todo: Read from env
BLOB_STORE_TYPE = "local"


class MediaUtils:
    @staticmethod
    def save_video(video_file: bytes, path: Path) -> str:
        with open(path, "wb") as out_file:  # open for [w]riting as [b]inary
            out_file.write(video_file)
        return path


class BlobStore:
    def __init__(self, store_type: str = None, bucket_name: str = None) -> None:
        self.store_type = BLOB_STORE_TYPE if not store_type else store_type
        self.bucket_name = config("BUCKET_NAME") if not bucket_name else bucket_name

    def _get_abs_path(self, file_name: str, task: str):
        # @todo-low: add support for store-type s3
        return os.path.join(self.bucket_name, task, file_name)

    def _safe_open_wb(self, path):
        """
        Open "path" for writing, creating any parent directories as needed.
        """
        os.makedirs(os.path.dirname(path), exist_ok=True)
        return open(path, "wb")

    def write_file(self, file: bytes, file_name: str, task: str) -> None:
        """
        Write a file to file_name.
        How to use: Say you want to store `file` with `test.jpg` to `parent/child/test.jpg`,
        then call write_file(file, 'test.jpg', 'parent', 'child')
        """
        file_path = self._get_abs_path(file_name, task)
        with self._safe_open_wb(file_path) as f:
            f.write(file)

    def read_file(self, file_name: str, task: str) -> bytes:
        file_path = self._get_abs_path(file_name, task)
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        return file_bytes


## --------- example usage ------------
# bs = BlobStore()
# fl = open("/home/k2/Work/SCU/Distributed Systems/distributed-video-processing/distributed_video/load_balancer/app.py", "rb")
# fbytes = fl.read()
# bs.write_file(fbytes, "app.py", "parent", "child")
