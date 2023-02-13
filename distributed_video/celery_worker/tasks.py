from distributed_video.celery_worker.celery import app


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def process_video():
    print("Starting to process the video")
    return True
