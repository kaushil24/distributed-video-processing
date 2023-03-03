# @todo: script to automate starting the rabbitmq, celery and VP server.
# techincally dockerfile should call this script and and the envvars going into the
# dockerfile (and eventually into this script) should come from the docker-compose.yaml

# @todo: The way this script will work is something like this:
# docker run -d -p ${NODE_RBMQ_PORT}:5672 rabbitmq # start rabbitmq
# celery -A app.celery worker --loglevel=INFO  
# python app.py

# To have multiple nodes use the same script to start you need to decouple the following env vars
# this is a "good-enough" list but not an exhaustive one
# RABBIT_MQ_URL
# NODE_URL
# REQUEST_SOCKET_URL
# RESP_SOCKET_URL # however this one will be shared among all the nodes as we have only 1 queue where all the nodes will drop their results after processing the frame. LB will read from here
