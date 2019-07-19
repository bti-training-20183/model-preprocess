import numpy as np
import pandas as pd
from preprocessing_utils import *

class DataCleaning():
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename
        self.data_frame = pd.read_csv(csv_filename)
    
    def handle_missing_data(self):
        self.data_frame.fillna(0)

    def _detect_outliers(self, signal, threshold=2.0):
        detected = []
        for i in range(len(signal)):
            if np.abs(signal[i]) > threshold:
                detected.append(i)
        return detected

    def handle_outlier_data(self):
        signal = np.copy(self.data_frame.Close.values)
        std_signal = (signal - np.mean(signal)) / np.std(signal)
        outlier_points = self._detect_outliers(std_signal)
        self.data_frame = self.data_frame.drop(outlier_points, axis=0)

    def drop_unwanted_columns(self):
        unwanted_columns = ['Date', 'OpenInt']
        self.data_frame.drop(unwanted_columns, axis=1)

    def save_preprocessed_file(self, path_file):
        self.data_frame.to_csv(path_file, header=None, index=False)
