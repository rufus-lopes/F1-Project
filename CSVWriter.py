from UDP_unpacker import unpackUDPpacket
import threading
import matplotlib.pyplot as plt
import csv
import numpy as np
import pandas as pd
from databaseUnpacker import localFormat


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





class masterWriter(object):
    def __init__(self, _sessionUID):
        self.sessionUID = _sessionUID
        self.files = [f'SQL_Data/{self.sessionUID}/motion.csv', f'SQL_Data/{self.sessionUID}/lap.csv',
         f'SQL_Data/{self.sessionUID}/setup.csv', f'SQL_Data/{self.sessionUID}/telemetry.csv', f'SQL_Data/{self.sessionUID}/status.csv'] #not including event data in master table
        self.seperateData = []
        self.headers = []
        self.motion = None
        self.lap = None
        self.event = None
        self.setup = None
        self.telemetry = None
        self.status = None
        self.filteredDF
        self.master = None
    def read(self):
        '''reading the data into a DataFrame''' #consider using numpy if this is slow
        for file in self.files:
            self.seperateData.append(pd.read_csv(file), index_col = False)

            # with open(file, 'r') as f:
            #     reader = csv.reader(f, delimeter = ',')
            #     self.headers.append(next(reader))
            #     self.seperateData.append(np.array(list(reader)).astype(float))
    def sorter(self):
        motionCols = ["frameIdentifier", "worldPositionX", "worldPositionY", "worldPositionZ",
            "worldVelocityX", "worldVelocityY", "worldVelocityZ", "yaw", "pitch", "roll"]

        lapCols= ["frameIdentifier", "lastLapTime", "currentLapTime", "bestLapTime", "currentLapNum", "finalLapTime"]

        setupCols = [ "Index", "frameIdentifier", "SessionTime", "frontWing", "rearWing", "onThrottle", "offThrottle", "frontCamber",
        "rearCamber", "frontToe", "rearToe", "frontSuspension", "rearSuspension", "frontAntiRollBar",
        "rearAntiRollBar", "frontSuspensionHeight", "rearSuspensionHeight", "brakePressure", "brakeBias",
        "rearLeftTyrePressure", "rearRightTyrePressure", "frontLeftTyrePressure", "frontRightTyrePressure",
        "ballast","fuelLoad"]

        telemetryCols = ["frameIdentifier", "speed", "throttle", "steer", "brake", "clutch", "gear", "engineRPM",
        "drs", "brakesTemperatureRL", "brakesTemperatureRR", "brakesTemperatureFL", "brakesTemperatureFR",
        "tyresSurfaceTemperatureRL", "tyresSurfaceTemperatureRR",
        "tyresSurfaceTemperatureFL", "tyresSurfaceTemperatureFR", "engineTemperature"]

        statusCols = ["frameIdentifier", "fuelMix", "FrontBrakeBias", "fuelInTank", "fuelRemainingLaps",
        "tyresWearRL", "tyresWearRR", "tyresWearFL", "tyresWearFR", "actualTyreCompound", "tyresAgeLaps"]
        sessionCols = ['frameIdentifier', 'weather', 'trackTemperature', 'trackLength', 'trackId']

        filterColumns = [motionCols, lapCols, setupCols, telemetryCols, statusCols]
        for i in range(len(self.seperateData)):
            df = self.seperateData[i]
            self.filteredDF.append(df[filterColumns[i]])

        self.motion, self.lap, self.setup, self.telemetry, self.status = self.filteredDF
        self.master = self.motion.merge(self.lap, on='frameIdentifier')
        #self.master = self.master.merger(self.setup, on='frameIdentifier') not using setup in master. Need to create a seperate session and setup live master csv
        self.master = self.master.merge(self.telemetry, on='frameIdentifier')
        self.master = self.master.mergre(self.status, on='frameIdentifier')
    def writer(self):
        self.master.to_csv(f'SQL_Data/{self.sessionUID}/master.csv')
