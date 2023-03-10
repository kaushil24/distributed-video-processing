# Starting the video processor (node)

## For multi-nodes setup

### Node-1:
1. Create a copy of the `.env.node1.example` file and rename it to `.env.node1`
   1. As convention for this project, use the following values
    ```shell
    NODE_ID=1
    CELERY_BROKER_URL="amqp://localhost:5679"
    NODE_URL="http://0.0.0.0:5001"
    REQ_SOCKET_URL="127.0.0.1:9008"
    ```
2. Start the queue and celery
   **NOTE**: Make sure the port (5679 in this case) is same as the port in CELERY_BROKER_URL in .env.node1
    ```
    docker run -d -p 5679:5672 rabbitmq
    source .env.node1 .env.shared && celery -A app.celery -b ${CELERY_BROKER_URL} worker --concurrency=1  --loglevel=INFO
    ```
    - Single worker because at the end of the queue, we pass an EOF signal that tells to commit everything to the db. If multiple workers are running and if one worker reads EOF, it will commit to db and other workers will miss out commiting their part to the db.
    - This is a hacky workaround. Figure out some way that if one worker reads EOF it can publish it to other workers and signal them to commit their part to the db. @todo:
3. In a different terminal start the node server
   ```
   python3 app.py -nenv .env.node1 -senv .env.shared 
   ```

### Node-2:
1. Create a copy of the `.env.node2.example` file and rename it to `.env.node2`
   - As a convention for this project you can use the following values
    ```shell
    NODE_ID=2
    CELERY_BROKER_URL="amqp://localhost:5670"
    NODE_URL="http://0.0.0.0:5002"
    REQ_SOCKET_URL="127.0.0.1:9009"
    ```
    **NOTE**: Make sure the values here are in sync with the `.env` in parent dir.
2. In a new terminal start the queue and celery
   **NOTE**: Make sure the port (5670 in this case) is same as the port in CELERY_BROKER_URL in .env.node2
    ```shell
    docker run -d -p 5670:5672 rabbitmq
    source .env.node2 .env.shared && celery -A app.celery -b ${CELERY_BROKER_URL} worker  --concurrency=1 --loglevel=INFO
    ```
3. In a different terminal start the node server
   ```shell
   python3 app.py -nenv .env.node2 -senv .env.shared 
   ```
