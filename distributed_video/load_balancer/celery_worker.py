from celery import Celery
from decouple import config


CELERY_BROKER_URL = config("LB_CELERY_BROKER_URL")
CELERY_BACKEND_URL = config("LB_CELERY_BACKEND_URL")
celery_app = Celery(
    "load_balancer",
    broker=CELERY_BROKER_URL,
    include=["distributed_video.load_balancer.load_balancer"],
    backend=CELERY_BACKEND_URL,
)
