from decouple import config


CELERY_QUEUE = config("LB_CELERY_QUEUE")
RESP_SOCKET_URL = config("RESP_SOCKET_URL")
