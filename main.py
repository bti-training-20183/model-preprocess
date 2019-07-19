from utils.datastore_handler import DataStore_Handler
from utils.message_handler import Message_Handler
from utils.database_handler import Database_Handler
from preprocess_input import *
from preprocessing_utils import *
import os
import sys
import config
import json
import time
sys.path.append(os.getcwd())


def callback(channel, method, properties, body):
    print(f'[x] Received {body} from {properties}')
    received_msg = json.loads(body)
    to_path = 'tmp/' + received_msg['name'] + received_msg['type']
    DataStore_Handler.download(received_msg['file_uri'], to_path)

    # PREPROCESSING DATA
    convert_file_to_csv(to_path)
    csv_filename = to_path.replace(received_msg['type'], '.csv')
    data_cleaning = DataCleaning(csv_filename)
    data_cleaning.handle_missing_data()
    data_cleaning.handle_outlier_data()
    data_cleaning.drop_unwanted_columns()
    data_cleaning.save_preprocessed_file(to_path)

    # THEN UPLOAD TO MINIO
    filename = received_msg['name']
    file_extension = received_msg['type']
    from_path = to_path  # dummy test
    to_path = filename + '/preprocessed/' + filename + '.csv'

    DataStore_Handler.upload(from_path, to_path)
    os.remove(from_path)
    # SAVE LOGS TO MONGO
    msg = {
        "name": filename,
        "type": file_extension,
        # TODO: Add Date
        "file_uri": to_path
    }
    # SEND MESSAGE TO MODEL CREATOR
    Message_Handler.sendMessage('from_preprocessor', json.dumps(msg))


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
