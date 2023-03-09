# distributed-video-processing

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
