from UDP_unpacker import unpackUDPpacket
import threading
import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
from databaseUnpacker import localFormat


class visualiser(threading.Thread):
    def __init__(self, _sessionUID):
        super().__init__(name="visualiser")
        self.packet = None
        self.unpacked = None
        self.type = None
        self.sessionUID = _sessionUID
        self.fileName = "CSV_Data/" + str(_sessionUID) + ".csv"
    def accept_packet(self, packet):
        self.packet = packet
        self.unpacked = unpackUDPpacket(self.packet)
        self.type = self.unpacked.header.packetId
        self.sessionUID = self.unpacked.header.sessionUID
    def write(self):
        if self.type == 0:
            data = localFormat(self.unpacked, self.type)
            data = data.arr
            with open(self.fileName, 'a') as file:
                writer = csv.writer(file)
                writer.writerow(data)
