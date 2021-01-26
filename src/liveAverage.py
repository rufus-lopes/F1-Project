import threading
import pandas as pd
import csv
from src.live import liveMerged
from time import time
import pickle
from sklearn.preprocessing import StandardScaler
import numpy as np

class liveAverage(threading.Thread):
    '''calculate the live average from the liveMerged'''
    def __init__(self, q, DONE):
        super().__init__(name='averages')

        self.q = q
        self.merged = pd.DataFrame()
        self.timeStep = 10
        self.roll = pd.DataFrame()
        self.sum = pd.DataFrame(dtype=np.float64)
        self.quitflag = False
        self.DONE = DONE
        self.input = pd.DataFrame()
        self.model = pickle.load(open('models/LinearRegression.pkl', 'rb'))

        self.columnsToSum = [
        'currentLapTime', 'worldPositionX', 'worldPositionY', 'worldPositionZ',
        'worldVelocityX', 'worldVelocityY', 'worldVelocityZ', 'yaw', 'pitch',
        'roll', 'speed', 'throttle', 'steer', 'brake', 'clutch', 'gear','engineRPM',
        'drs', 'brakesTemperatureRL', 'brakesTemperatureRR','brakesTemperatureFL',
        'brakesTemperatureFR',  'tyresSurfaceTemperatureRL','tyresSurfaceTemperatureRR',
        'tyresSurfaceTemperatureFL','tyresSurfaceTemperatureFR', 'engineTemperature',
        'tyresWearRL', 'tyresWearRR', 'tyresWearFL', 'tyresWearFR', 'carPosition'
        ]

        self.summedColumns = ['summed_'+ name for name in self.columnsToSum]
    def reader(self):
        fullQ = [self.q.get() for i in range(self.q.qsize())]
        if fullQ:
            self.merged = fullQ[-1]
        if self.merged is self.DONE: #session has ended
            self.q.task_done()
            self.merged = pd.DataFrame()
    def averager(self):
        if not self.merged.empty:
            self.roll = self.merged.rolling(self.timeStep, min_periods=1).mean()
    def summer(self):
        if not self.merged.empty:
            df = self.merged[self.columnsToSum]
            self.sum = df.cumsum()
            self.sum.columns = self.summedColumns
            self.sum = self.sum.astype(np.float64)
    def writer(self):
        if not self.roll.empty:
            self.input = pd.concat([self.roll, self.sum], axis=1)
    def predictor(self):
        if self.input.shape[0] > 2:
            pred = self.model.predict(self.input)
            print(np.mean(pred))
    def run(self):
        while not self.quitflag:
            self.reader()
            self.averager()
            self.summer()
            self.writer()
            self.predictor()
        print(self.input.info())
        print(self.input)
        self.input.to_csv('CSV_Data/av.csv')

    def requestQuit(self):
        self.quitflag = True
