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
  - Create a `distributed-video.pth` file in `.venv/lib/{python-version}/site-packages`. Paste this `/home/k2/Work/SCU/Distributed Systems/distributed-video-processing/distributed_video`
- Set up pre-commit hooks. Run `pre-commit install`

- Setting up env vars:
   1. Make a copy of `.env.example` and rename to `.env`.
   2. Update the contents
