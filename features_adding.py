import pandas as pd
import numpy as np
from preprocessing_utils import *

class FeaturesAdding():
    def __init__(self, data_frame):
        self.data_frame = data_frame

    def add_momentum_1D(self):
        self.data_frame['Momentum_1D'] = (self.data_frame['Close'] - self.data_frame['Close'].shift(1)).fillna(0)
    
    def add_RSI_14D(self):
        self.data_frame['RSI_14D'] = \
            self.data_frame['Momentum_1D'].rolling(center=False, window=14).apply(calculate_rsi).fillna(0)
    
    def add_volume_plain(self):
        self.data_frame['Volume_plain'] = self.data_frame['Volume']

    def add_BB_band(self):
        self.data_frame['BB_Midle_band'], self.data_frame['BB_Upper_band'], self.data_frame['BB_Lower_band'] = \
            bbands(self.data_frame['Close'], length = 20, numsd=1)
        self.data_frame['BB_Midle_band'] = self.data_frame['BB_Midle_band'].fillna(0)
        self.data_frame['BB_Upper_band'] = self.data_frame['BB_Upper_band'].fillna(0)
        self.data_frame['BB_Lower_band'] = self.data_frame['BB_Lower_band'].fillna(0)

    def add_Aroon_Oscillator(self):
        list_of_zeros = [0]*25
        up, down = aroon(self.data_frame)
        aroon_list = [x - y for x,y in zip(up, down)]
        if len(aroon_list) == 0:
            aroon_list = [0]*self.data_frame.shape[0]
            self.data_frame['Aroon_Oscillator'] = aroon_list
        else:
            self.data_frame['Aroon_Oscillator'] = list_of_zeros + aroon_list

    def add_PVT(self):
        self.data_frame['PVT'] = \
            (self.data_frame['Momentum_1D']/self.data_frame['Close'].shift(1))*self.data_frame['Volume']
        self.data_frame['PVT'] = self.data_frame['PVT'] - self.data_frame['PVT'].shift(1)
        self.data_frame['PVT'] = self.data_frame['PVT'].fillna(0)

    def add_PSAR(self):
        psar(self.data_frame)

    def add_CMFlow(self):
        listofzeros = [0] * 40
        CHMF = CMFlow(self.data_frame, 20)
        if len(CHMF) == 0:
            CHMF = [0] * self.data_frame.shape[0]
            self.data_frame['Chaikin_MF'] = CHMF
        else:
            self.data_frame['Chaikin_MF'] = listofzeros + CHMF

    def add_ROC(self):
        self.data_frame['ROC'] = ((self.data_frame['Close'] - self.data_frame['Close'].shift(12)) / (
            self.data_frame['Close'].shift(12))) * 100
        self.data_frame = self.data_frame.fillna(0)

    def add_VWAP(self):
        self.data_frame['VWAP'] = np.cumsum(self.data_frame['Volume'] * (
                    self.data_frame['High'] + self.data_frame['Low']) / 2) / np.cumsum(
            self.data_frame['Volume'])
        self.data_frame = self.data_frame.fillna(0)

    def add_CCI(self):
        self.data_frame['CCI'] = CCI(self.data_frame, 20, 0.015)
        self.data_frame = self.data_frame.fillna(0)

    def add_OBV(self):
        new = (self.data_frame['Volume'] * (~self.data_frame['Close'].diff().le(0) * 2 - 1)).cumsum()
        self.data_frame['OBV'] = new

    def add_KELCH(self):
        KelchM, KelchD, KelchU = KELCH(self.data_frame, 14)
        self.data_frame['Kelch_Upper'] = KelchU
        self.data_frame['Kelch_Middle'] = KelchM
        self.data_frame['Kelch_Down'] = KelchD
        self.data_frame = self.data_frame.fillna(0)

    def add_EMA(self):
        self.data_frame['EMA'] = self.data_frame['Close'].ewm(span=3, min_periods=0, adjust=True,
                                                                        ignore_na=False).mean()
        self.data_frame = self.data_frame.fillna(0)
        self.data_frame['TEMA'] = (3 * self.data_frame['EMA'] - 3 * self.data_frame['EMA'] *
                                        self.data_frame['EMA']) + (
                                                   self.data_frame['EMA'] * self.data_frame['EMA'] *
                                                   self.data_frame['EMA'])

    def add_NATR(self):
        self.data_frame['HL'] = self.data_frame['High'] - self.data_frame['Low']
        self.data_frame['absHC'] = abs(self.data_frame['High'] - self.data_frame['Close'].shift(1))
        self.data_frame['absLC'] = abs(self.data_frame['Low'] - self.data_frame['Close'].shift(1))
        self.data_frame['TR'] = self.data_frame[['HL', 'absHC', 'absLC']].max(axis=1)
        self.data_frame['ATR'] = self.data_frame['TR'].rolling(window=14).mean()
        self.data_frame['NATR'] = (self.data_frame['ATR'] / self.data_frame['Close']) * 100
        self.data_frame = self.data_frame.fillna(0)

    def add_DMI(self):
        DMI(self.data_frame, 14)
        self.data_frame = self.data_frame.fillna(0)

    def drop_unwanted_columns(self):
        columns2Drop = ['UpMove', 'DownMove', 'ATR', 'PlusDM', 'MinusDM', 'Zero', 'EMA', 'HL', 'absHC', 'absLC', 'TR']
        self.data_frame = self.data_frame.drop(labels=columns2Drop, axis=1)