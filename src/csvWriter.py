from src.UDP_unpacker import unpackUDPpacket
import threading
import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
from src.databaseUnpacker import localFormat
import logging
import ctypes
import time

class csvWriter(object):
    def __init__(self, _sessionUID):
        self.packet = None
        self.unpacked = None
        self.type = None
        self.sessionUID = _sessionUID
        self.fileName = None            #"CSV_Data/" + str(self.sessionUID) + ".csv"
    def accept_packet(self, packet):
        self.packet = packet
        self.unpacked = unpackUDPpacket(self.packet)
        self.type = self.unpacked.header.packetId
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
        data = localFormat(self.unpacked, self.type).arr
        fileName = f"CSV_Data/{self.sessionUID}/motion.csv"
        with open(fileName, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)

    def session(self):
        data = localFormat(self.unpacked, self.type).arr
        fileName = f"CSV_Data/{self.sessionUID}/session.csv"
        with open(fileName, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    def lap(self):
        data = localFormat(self.unpacked, self.type).arr
        fileName = f"CSV_Data/{self.sessionUID}/lap.csv"
        with open(fileName, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    def event(self):
        data = localFormat(self.unpacked, self.type).arr
        fileName = f"CSV_Data/{self.sessionUID}/event.csv"
        with open(fileName, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    def participants(self):
        pass
    def setup(self):
        data = localFormat(self.unpacked, self.type).arr
        fileName = f"CSV_Data/{self.sessionUID}/setup.csv"
        with open(fileName, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    def telemetry(self):
        data = localFormat(self.unpacked, self.type).arr
        fileName = f"CSV_Data/{self.sessionUID}/telemetry.csv"
        with open(fileName, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    def status(self):
        data = localFormat(self.unpacked, self.type).arr
        fileName = f"CSV_Data/{self.sessionUID}/status.csv"
        with open(fileName, 'a') as file:
            writer = csv.writer(file)
            writer.writerow(data)
    def finalClassification(self):
        pass
    def lobbyInfo(self):
        pass

class masterWriter(threading.Thread):
    def __init__(self, _sessionUID):
        super().__init__(name="CSVWriter")
        self.sessionUID = _sessionUID
        self.files = [
        f'CSV_Data/{self.sessionUID}/motion.csv',
        f'CSV_Data/{self.sessionUID}/lap.csv',
        f'CSV_Data/{self.sessionUID}/setup.csv',
        f'CSV_Data/{self.sessionUID}/telemetry.csv',
        f'CSV_Data/{self.sessionUID}/status.csv'
        ] #not including event data in master table
        self.seperateData = []
        self.previousRows = [0]*5
        self.headers = []
        self.motion = None
        self.lap = None
        self.event = None
        self.setup = None
        self.telemetry = None
        self.status = None
        self.master = None
        self.quitflag = False
        self.first = True

        self.motionCols = ["frameIdentifier", "worldPositionX", "worldPositionY", "worldPositionZ",
            "worldVelocityX", "worldVelocityY", "worldVelocityZ", "yaw", "pitch", "roll"]

        self.lapCols= ["frameIdentifier", "lastLapTime", "currentLapTime", "bestLapTime", "currentLapNum"]

        self.setupCols = ["frameIdentifier", "SessionTime", "frontWing", "rearWing", "onThrottle", "offThrottle", "frontCamber",
        "rearCamber", "frontToe", "rearToe", "frontSuspension", "rearSuspension", "frontAntiRollBar",
        "rearAntiRollBar", "frontSuspensionHeight", "rearSuspensionHeight", "brakePressure", "brakeBias",
        "rearLeftTyrePressure", "rearRightTyrePressure", "frontLeftTyrePressure", "frontRightTyrePressure",
        "ballast","fuelLoad"]

        self.telemetryCols = ["frameIdentifier", "speed", "throttle", "steer", "brake", "clutch", "gear", "engineRPM",
        "drs", "brakesTemperatureRL", "brakesTemperatureRR", "brakesTemperatureFL", "brakesTemperatureFR",
        "tyresSurfaceTemperatureRL", "tyresSurfaceTemperatureRR",
        "tyresSurfaceTemperatureFL", "tyresSurfaceTemperatureFR", "engineTemperature"]

        self.statusCols = ["frameIdentifier", "fuelMix", "frontBrakeBias", "fuelInTank", "fuelRemainingLaps",
        "tyresWearRL", "tyresWearRR", "tyresWearFL", "tyresWearFR", "actualTyreCompound", "tyresAgeLaps"]
        sessionCols = ['frameIdentifier', 'weather', 'trackTemperature', 'trackLength', 'trackId']

        self.filterColumns = [self.motionCols, self.lapCols, self.setupCols, self.telemetryCols, self.statusCols]

        self.filteredDF = [pd.DataFrame(columns=cols) for cols in self.filterColumns]
    def reader(self):
        #consider using numpy if this is slow

        for i in range(len(self.files)):
            with open(self.files[i], 'r') as file:
                reader = list(csv.reader(file))
                data = reader[self.previousRows[i]+1:]
                header = reader[0]
                self.previousRows[i] = len(reader)
                self.seperateData.append(pd.DataFrame(data, columns = header))

    def sorter(self):

        for i in range(len(self.files)):
            df = self.seperateData[i]
            self.filteredDF[i] = pd.concat([self.filteredDF[i],df[self.filterColumns[i]]], ignore_index=True)
        self.motion, self.lap, self.setup, self.telemetry, self.status = self.filteredDF
        self.master = self.motion.merge(self.lap, on='frameIdentifier')
        self.master = self.master.merge(self.telemetry, on='frameIdentifier')
        self.master = self.master.merge(self.status, on='frameIdentifier')
        self.seperateData = []

    def writer(self):

        self.master.to_csv(f'CSV_Data/{self.sessionUID}/master.csv')

    def run(self):

        logging.info("Master CSV writer thread started")
        while True:
    
            self.reader()
            self.sorter()
            self.writer()
            if self.quitflag == True:
                break

        logging.info("CSV Writer thread stopped")


    def requestQuit(self, *args):

        if args:
            self.quitflag = True
