import threading
import pandas as pd
import csv
from src.live import liveMerged
from time import time
import pickle
from sklearn.preprocessing import StandardScaler
class liveAverage(threading.Thread):
    '''calculate the live average from the liveMerged'''
    def __init__(self, q, DONE):
        super().__init__(name="averages")
        self.q = q
        self.merged = pd.DataFrame()
        self.timeStep = 10
        self.roll = pd.DataFrame()
        self.sum = pd.DataFrame()
        self.quitflag = False
        self.DONE = DONE
        self.input = pd.DataFrame()
        self.model = pickle.load(open('models/LinearRegression.pkl', 'rb'))
        self.columnsToSum = [
        'currentLapTime', 'worldPositionX', 'worldPositionY', 'worldPositionZ',
        'worldVelocityX', 'worldVelocityY', 'worldVelocityZ', 'yaw', 'pitch',
        'roll', 'speed', 'throttle', 'steer', 'brake', 'clutch', 'gear',
        'engineRPM', 'drs', "brakesTemperatureRL", "brakesTemperatureRR",
        "brakesTemperatureFL", "brakesTemperatureFR",  "tyresSurfaceTemperatureRL",
        "tyresSurfaceTemperatureRR", "tyresSurfaceTemperatureFL",
        "tyresSurfaceTemperatureFR", 'engineTemperature',
        "tyresWearRL", "tyresWearRR", "tyresWearFL", "tyresWearFR", "carPosition"
        ]

        self.summedColumns = ['summed_'+ name for name in self.columnsToSum]
        self.sc = StandardScaler()
    def reader(self):
        fullQ = [self.q.get() for i in range(self.q.qsize())]
        if fullQ:
            self.merged = fullQ[-1]
        if self.merged is self.DONE:
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
    def writer(self):
        if not self.roll.empty:
            self.input = pd.concat([self.roll, self.sum], axis=1)
    def predictor(self):
        scaled = self.sc(self.input)
        data = scaled.iloc[-1]
        val = data
        print(self.model.predict([val]))
    def run(self):
        while not self.quitflag:
            self.reader()
            self.averager()
            self.summer()
            self.writer()
            #self.predictor()
        print(self.input.info())
        print(self.input)
        self.input.to_csv('CSV_Data/av.csv')

    def requestQuit(self):
        self.quitflag = True
