import threading
import pandas as pd
import csv

class liveAverage(threading.Thread):
    '''calculate the live average from the liveMerged'''
    def __init__(self, _sessionUID):
        super().__init__(name="averages")
        self.sessionUID = _sessionUID
        self.quitflag = False
        self.previousRows = 0
    def reader(self):

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
