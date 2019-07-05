import os
import sys
import config
import time
sys.path.append(os.getcwd())
from utils.message_handler import MessageHandler


def callback(channel, method, properties, body):
    print(f'[x] Received {body} from {properties}')
    MessageHdlr.sendMessage('from_creator', 'Dummy message from deployer')


class Preprocessor:
    def __init__(self):
        pass

    def listen(self, queue, MessageHandler):
        MessageHandler.consumeMessage(queue, callback)

if __name__ == "__main__":
    MessageHdlr = MessageHandler(config.RABBITMQ_CONNECTION)
    model_creator = Preprocessor()
    model_creator.listen(config.QUEUE["from_client"],MessageHdlr)