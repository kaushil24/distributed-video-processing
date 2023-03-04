# Starting the video processor (node)

1. Start the queue and celery
    ```
    docker run -d -p 5679:5672 rabbitmq
    celery -A app.celery worker --loglevel=INFO
    ```
2. In a different terminal start the node server
   ```
   python app.py
   ```
