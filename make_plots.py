import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import seaborn as sns

def create_time_series_features_plot(data_frame, plot_name):
    data_frame.index = pd.DatetimeIndex(freq='w', start=0, periods=len(data_frame))
    time_series_features = seasonal_decompose(data_frame['Close'], model='multiplicative')
    time_series_features.plot()
    plt.savefig(plot_name)

def create_correlation_plot(data_frame, plot_name):
    data_frame = data_frame.drop(['Date', 'OpenInt', 'Volume'], axis=1)
    corr = data_frame.corr()
    plt.figure(figsize=(16, 10))
    sns.heatmap(corr, annot=True, fmt=".4f")
    plt.savefig(plot_name)

def create_outliers_plot(data_frame, plot_name):
    def detect_outliers(signal, threshold=2.0):
        detected = []
        for i in range(len(signal)):
            if np.abs(signal[i]) > threshold:
                detected.append(i)
        return detected

    signal = np.copy(data_frame.Close.values)
    std_signal = (signal - np.mean(signal)) / np.std(signal)
    outliers = detect_outliers(std_signal)
    plt.figure(figsize=(15, 7))
    plt.plot(np.arange(len(data_frame.Close)), data_frame.Close)
    plt.plot(np.arange(len(data_frame.Close)), data_frame.Close, 'X', label='outliers', markevery=outliers, c='r')
    plt.legend()
    plt.savefig(plot_name)