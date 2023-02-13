# distributed-video-processing

## dev setup
- Install rabbit mq. This message broker is used by celery
  - `sudo apt-get install rabbitmq-server`
- Setting up venv and installing requirements
   ```shell
   cd distributed_video/
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
- Update python path to import `libs` across project  
  ```
   cd $(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")
   echo /home/kaushil/Work/SCU/DistSyst/Project/distributed-video-processing/distributed_video/libs > dist-vid-libs.pth
   ```
- Setting up venvs:
   1. Make a copy of `.env.example` and rename to `.env`.
   2. Update the contents
