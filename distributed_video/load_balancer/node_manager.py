import zmq
from typing import List
from decouple import config, Csv


class Node:
    def bind_socket(self) -> zmq.Socket:
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUSH)
        try:
            self.socket.bind(f"tcp://{self.req_socket_url}")
        except zmq.ZMQError as zqme:
            print("Port already binded")

    def __init__(self, base_url: str, req_socket_url: str) -> None:
        # req_socket_url is the url on which this node is expceted to recieve incoming (requests) messages
        # aka the url on which the LB is expected to push the messages for that node to listen
        self.base_url = base_url
        self.req_socket_url = req_socket_url
        self.bind_socket()

    def close_socket(self):
        self.socket.close()
        self.context.destroy()


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
        req_socket_url = config("REQ_SOCKET_URLS", cast=Csv())
        nodes_urls = config("NODES", cast=Csv())
        nodes = []
        for node_url, socket_url in zip(nodes_urls, req_socket_url):
            nodes.append(Node(node_url, socket_url))
        return nodes

    def send_json(self, *args, **kwargs):
        """
        Wrapper over socket.send_json(). It picks the socket pointed
        by the next
        """
        resp = self.nodes[self.next_node_index].socket.send_json(*args, **kwargs)
        self.increment_next_node_index()
        return resp

    def increment_next_node_index(self) -> None:
        self.next_node_index = (self.next_node_index + 1) % self.num_nodes

    def close_all_sockets(self):
        for node in self.nodes:
            node.close_socket()

    def bind_all_sockets(self):
        for node in self.nodes:
            node.bind_socket()
