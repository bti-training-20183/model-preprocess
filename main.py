from utils.datastore_handler import DataStore_Handler
from utils.message_handler import Message_Handler
import os
import sys
import config
import time
import json
sys.path.append(os.getcwd())


def callback(channel, method, properties, body):
    print(f'[x] Received {body} from {properties}')
    msg = json.loads(body)
    to_path = 'tmp/' + msg['name']
    DataStore_Handler.download(msg['file_uri'],to_path)
    # TO DO: PREPROCESSING DATA
    # SAVE LOGS TO MONGO
    # THEN UPLOAD TO MINIO
    # SEND MESSAGE TO MODEL CREATOR
    # Message_Handler.sendMessage('from_preprocessor', 'Dummy message from preprocessor')

class Preprocessor:
    def __init__(self):
        pass

    def listen(self, queue, MessageHandler):
        Message_Handler.consumeMessage(queue, callback)


if __name__ == "__main__":
    if not os.path.exists('tmp'):
        os.makedirs('tmp')
    model_preprocessor = Preprocessor()
    model_preprocessor.listen(config.QUEUE["from_client"], callback)
