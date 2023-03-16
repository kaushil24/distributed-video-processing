import cv2
from distributed_video.libs.utils import BlobStore
import os


def aggregator(task_id, total_frames):
    img_array = []
    bs = BlobStore()
    # file_list = glob.glob("/home/k2/Work/SCU/Distributed Systems/distributed-video-processing/distributed_video/bucket/"+task_id+"/*.jpg")
    # print(file_list)
    # for filename in file_list:
    for i in range(total_frames):
        img = bs.read_frame(f"{i}.jpg", task_id)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    print(len(img_array))
    save_path = os.path.join("media", str(task_id) + ".avi")
    out = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*"MJPG"), 15, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    return "success"
