from celery import Celery

app = Celery('celery_worker',
             broker='pyamqp://guest@localhost//',
             backend='rpc://',
             # Use absolute path!!
             include=['distributed_video.celery_worker.tasks'])

# Optional configuration, see the application user guide.
app.conf.update(
    result_expires=3600,
)

if __name__ == '__main__':
    app.start()
