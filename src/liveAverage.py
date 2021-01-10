import threading
import pandas as pd
import csv

class liveAverage(threading.Thread):
    def __init__(self, _sessionUID):
        super().__init__(name="averages")
        self.sessionUID = _sessionUID
        self.quitflag = False
        self.previousRows = 0
    def reader(self):
        with open("SQL_Data/{self.sessionUID}/master.csv", 'r') as f:
            reader = csv.reader(f)
            data = list(reader)[self.previousRows:]
            headers = list(reader)[0]
            self.previousRows = len(list(reader))

    def grouper(self):
        pass
    def averager(self):
        pass
    def summer(self):
        pass
    def writer(self):
        pass
    def run(self):
        pass
    def requestQuit(self):
        self.quitflag = True
