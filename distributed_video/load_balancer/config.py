from decouple import config, Csv
from typing import List

NUM_NODES = 'NUM_NODES'
NODES_IP = 'NODES_IP'

class LoadBalancerConfig:
    num_nodes = config(NUM_NODES, cast=int)
    nodes_ip = config(NODES_IP, cast=Csv())
