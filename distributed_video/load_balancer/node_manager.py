import zmq
from typing import List
from decouple import config, Csv


class Node:
    def _bind_socket(self) -> zmq.Socket:
        context = zmq.Context()
        self.socket = context.socket(zmq.PUSH)
        self.socket.bind(f"tcp://{self.recv_socket_url}")

    def __init__(self, base_url: str, recv_socket_url: str) -> None:
        # recv_socket_url is the url on which this node is expceted to recieve incoming messages
        # aka the url on which the LB is expected to push the messages for  that node to listen
        self.base_url = base_url
        self.recv_socket_url = recv_socket_url
        self._bind_socket()


class NodesDirectory:
    def __init__(self) -> None:
        self.nodes: List[Node] = self.node_discovery()
        self.next_node_index: int | None = 0
        self.num_nodes = len(self.nodes)
        # next_node_index points to the node that shall be used
        # to send the message. This comes in handy when we're sending
        # rotationally

    @staticmethod
    def node_discovery() -> List[Node]:
        # @todo: Implement health check before discovery
        recv_socket_urls = config("RECV_SOCKET_PORTS", cast=Csv())
        nodes_urls = config("NODES", cast=Csv())
        nodes = []
        for node_url, socket_url in zip(nodes_urls, recv_socket_urls):
            nodes.append(Node(node_url, socket_url))
        return nodes

    def increment_next_node_index(self) -> None:
        self.next_node_index = (self.next_node_index + 1) % self.num_nodes
