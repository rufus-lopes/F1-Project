from UDP_unpacker import unpackUDPpacket
import threading
import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
from databaseUnpacker import localFormat


class csvWriter(threading.Thread):
    def __init__(self, _sessionUID):
        super().__init__(name="visualiser")
        self.packet = None
        self.unpacked = None
        self.type = None
        self.sessionUID = _sessionUID
        self.fileName = None            #"CSV_Data/" + str(self.sessionUID) + ".csv"
    def accept_packet(self, packet):
        self.packet = packet
        self.unpacked = unpackUDPpacket(self.packet)
        self.type = self.unpacked.header.packetId
        self.sessionUID = self.unpacked.header.sessionUID
    def write(self):
        type_to_function = {0:"motion", 1:"session", 2:"lap", 3:"event", 4:"participants",
        5:"setup", 6:"telemetry", 7:"status", 8:"finalClassification", 9:"lobbyInfo"}
        getattr(csvWriter, type_to_function[self.type])(self)
        # if self.type == 0:
        #     data = localFormat(self.unpacked, self.type)
        #     data = data.arr
        #     with open(self.fileName, 'a') as file:
        #         writer = csv.writer(file)
        #         writer.writerow(data)
    def motion(self):
        print("motion")
        pass
    def session(self):
        print("session")
        pass
    def lap(self):
        print("lap")
        pass
    def event(self):
        print("event") 
        pass
    def participants(self):
        pass
    def setup(self):
        pass
    def telemetry(self):
        pass
    def status(self):
        pass
    def finalClassification(self):
        pass
    def lobbyInfo(self):
        pass
