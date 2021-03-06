import threading
import pandas as pd
import csv
from src.live import liveMerged
from time import time

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

        self.columnsToSum = [
        'currentLapTime', 'worldPositionX', 'worldPositionY', 'worldPositionZ',
        'worldVelocityX', 'worldVelocityY', 'worldVelocityZ', 'yaw', 'pitch',
        'roll', 'speed', 'throttle', 'steer', 'brake', 'clutch', 'gear',
        'engineRPM', 'drs', "brakesTemperatureRL", "brakesTemperatureRR",
        "brakesTemperatureFL", "brakesTemperatureFR",  "tyresSurfaceTemperatureRL",
        "tyresSurfaceTemperatureRR", "tyresSurfaceTemperatureFL",
        "tyresSurfaceTemperatureFR", 'engineTemperature',
        "tyresWearRL", "tyresWearRR", "tyresWearFL", "tyresWearFR"
        ]

        self.summedColumns = ['summed_'+ name for name in self.columnsToSum]

    def reader(self):
        fullQ = [self.q.get() for i in range(self.q.qsize())]
        if fullQ:
            self.merged = fullQ[-1]
        if self.merged is self.DONE:
            self.q.task_done()
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
    def run(self):
        while not self.quitflag:
            # t = time()
            self.reader()
            self.averager()
            self.summer()
            self.writer()
            # t2 = time() - t
            # print('averger time: ', t2)
        self.q.task_done()

        print(self.input.info())
        print(self.input)
        self.input.to_csv('CSV_Data/av.csv')

    def requestQuit(self):
        self.quitflag = True
