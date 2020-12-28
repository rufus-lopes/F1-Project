from UDP_unpacker import unpackUDPpacket
import threading
import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd

class visualiser(threading.Thread):
    def __init__(self):
        super().__init__(name="visualiser")
        self.packet = None
        self.unpacked = None
        self.type = None
        self.sessionUID = None
    def accept_packet(self, packet):
        self.packet = packet
        self.unpacked = unpackUDPpacket(self.packet)
        self.type = self.unpacked.header.packetId
        self.sessionUID = self.unpacked.header.sessionUID
    def write(self, writer):
        fileName = str(self.sessionUID) + ".csv"

        if self.type == 0:
            data = self.unpacked.carMotionData[0]
            speed = np.sqrt(data.worldVelocityX**2 + data.worldVelocityY**2 + data.worldVelocityZ**2)
            time = self.unpacked.header.sessionTime
            writer.writerow([time, speed])
            df = pd.read_csv(fileName)
            plt.plot(df)
            plt.show()
