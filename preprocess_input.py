import numpy as np
import pandas as pd
from preprocessing_utils import *

class DataCleaning():
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename
        self.data_frame = pd.read_csv(csv_filename)
    
    def handle_missing_data(self):
        self.data_frame.fillna(0)

    def handle_outlier_data(self):
        # TODO
        pass

