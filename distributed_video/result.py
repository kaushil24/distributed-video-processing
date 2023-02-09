import time
import zmq
import pprint

def result_collector():
    context = zmq.Context()
    results_receiver = context.socket(zmq.PULL)
    results_receiver.bind("tcp://127.0.0.1:5558")

    consumer_sender = context.socket(zmq.PUSH)
    consumer_sender.connect("tcp://127.0.0.1:6000")
    while True:
        result = results_receiver.recv_json()
        print(result)
        consumer_sender.send_json(result)
        print("Sent")


result_collector()