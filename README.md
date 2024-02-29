# distributed-video-processing
- Distributed Video Processing is a system designed to to apply face filters in a distributed and parallelized manner. The project consists of three key components: a Load Balancer, Nodes (microservices), and an Aggregator.

### Key Components
1. Load Balancer:
  - Receives video input.
  - Breaks down the video into individual frames.
  - Distributes frames to multiple nodes for parallel processing.
2. Nodes (Microservices):
  - Receive individual frames from the load balancer.
  - Apply face filters independently.
  - Operate in parallel for efficient processing.

3. Aggregator (Microservice):
  - Gathers processed frames from all nodes.
  - Merges frames into the final video with applied face filters.

This microservices-based architecture ensures modularity, scalability, and improved performance, making it easy to update and scale specific components independently. The result is a streamlined process that efficiently enhances video content with face filters.

### High level overview
![High Level Overview](https://media.discordapp.net/attachments/1119444495071719497/1192736607984435210/high-level-architecture.png?ex=65aa2987&is=6597b487&hm=cd7fdbbd247c36adcfc1aa2b7de7fbf13fea0d34bcdc79ae485d5b1e3eb515fc&=&format=webp&quality=lossless&width=1634&height=618)

### Networking Overview
![image](https://github-production-user-asset-6210df.s3.amazonaws.com/39802957/309045081-35e9fd8f-1cf8-4e88-a63a-cb6491e48204.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20240229%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240229T191002Z&X-Amz-Expires=300&X-Amz-Signature=b30609a7efe55d0e5a922120b915f6a474e3d057dff601f1abf054dc82b42c55&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=0)

### Code Organization
![Code Organization](https://raw.githubusercontent.com/kaushil24/distributed-video-processing/main/code-organization.png)

## dev setup
- Install rabbit mq. This message broker is used by celery
  - `sudo apt-get install rabbitmq-server`
- Setting up venv and installing requirements
   ```shell
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
- Update add distributed_video to python path.
  - Create a `distributed-video.pth` file in `.venv/lib/{python-version}/site-packages`. Paste this `/home/phani/Desktop/disributed/project/distributed-video-processing/distributed_video
`
- Set up pre-commit hooks. Run `pre-commit install`
- Set project root. Add the following line in ~/.bashrc `DIST_VIDEO_PROJECT_ROOT=/home/k2/Work/SCU/Distributed Systems/distributed-video-processing`


## Starting pgsql
- `sudo docker run --name dist-pg -e POSTGRES_USER="postgres" -e POSTGRES_PASSWORD="HeLL0WZ" -e POSTGRES_DB="distvdo"  postgres` 
- Run the following command to get the url: `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dist-pg`
- Copy the IP and put it in the .env file: `SQLALCHEMY_DATABASE_URI="postgresql+psycopg2://${POSTGRES_USER}:${POSTGRES_PASSWORD}@<IP>:5432/${POSTGRES_DB}"`
  - **For restarting**: Shut down the container and then do `sudo docker rm dist-pg` 

## Starting the servers:
- Setting up env vars. These vars are mostly used by the LB:
   1. Make a copy of `.env.example` and rename to `.env`.
   2. Update the contents
- Setup env vars for nodes. `cd distributed_video/video_processor`
  - If there are i nodes in `.env` then THERE HAS TO BE `.env.node[i]` in video_processor.
  - Make sure you have `.env.node[i]` and `.env.shared` configured correctly. Refer `.env.node.example` and `.env.shared.example` for list of all the config


### Starting the LB

```shell
  cd distributed_video/load_balancer`
  python app.py
```

### Starting Video processor
- Refer to the readme.md in video_processor


Usually for the developement workflow, you only need to star the VP and use NodeDirector and/or LoadBalancer classes. Refer to `video-sender.test.ipynb` and `scratchpad.test.ipynb` to see how to use them. You don't need to have the LB server running UNLESS you want to do E2E runs.

### Project Scope

- Get number of available worker machines
- Job completion time statistics to Db
- Store runtime of individual frame
- On UI:
  - display IP of each worker
  - unprocessed frame
  - completed frame on worker machine
  - avg time of completed job on a worker
