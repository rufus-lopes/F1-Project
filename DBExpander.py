import sqlite3
import pandas as pd
import struct
from datatypes import PacketID, EventStringCode
from UDP_unpacker import unpackUDPpacket
import os
import inspect
import ctypes
from databaseUnpacker import localFormat
import warnings
import numpy as np
import matplotlib
from addColumnNames import addColumnNames
import logging
from times import *

warnings.filterwarnings("ignore")

def connect(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def selectALL(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM packets ORDER BY pkt_id ASC")
    #cur.execute("PRAGMA table_info(packets)") #just checking table column names
    rows = cur.fetchall()
    df = pd.DataFrame(rows)
    return df


def globalFormater(df):
    packetTypes = df["packetId"]
    packets = df["packet"]
    packetIDs = df["pkt_id"]
    sessionIDs = df["sessionUID"]
    motionArr = []
    sessionArr = []
    lapDataArr = []
    eventArr = []
    participantsArr = []
    carSetupsArr = []
    carTelemetryArr = []
    carStatusArr =[]
    finalClassificationArr = []
    lobbyInfoArr = []

    for i in range(len(packetTypes)):
        packetType = packetTypes[i]
        packetIDrelation = packetIDs[i]
        packetSessionRelation = sessionIDs[i]
        packet = unpackUDPpacket(packets[i])
        formatted_info = localFormat(packet, packetType)

        if packetType == 0:
            motionArr.append(formatted_info.arr)
        elif packetType == 1:
            sessionArr.append(formatted_info.arr)
        elif packetType == 2:
            lapDataArr.append(formatted_info.arr)
        elif packetType == 3:
            eventArr.append(formatted_info.arr)
        elif packetType == 4:
            participantsArr.append(formatted_info.arr)
        elif packetType == 5:
            carSetupsArr.append(formatted_info.arr)
        elif packetType == 6:
            carTelemetryArr.append(formatted_info.arr)
        elif packetType == 7:
            carStatusArr.append(formatted_info.arr)
        elif packetType == 8:
            finalClassificationArr.append(formatted_info.arr)
        elif packetType == 9:
            lobbyInfoArr.append(formatted_info.arr)

    motionDF = pd.DataFrame(motionArr)
    sessionDF = pd.DataFrame(sessionArr)
    lapDataDF = pd.DataFrame(lapDataArr)
    eventDF = pd.DataFrame(eventArr)
    participantsDF = pd.DataFrame(participantsArr)
    carSetupsDF = pd.DataFrame(carSetupsArr)
    carTelemetryDF = pd.DataFrame(carTelemetryArr)
    carStatusDF = pd.DataFrame(carStatusArr)
    finalClassificationDF = pd.DataFrame(finalClassificationArr)
    lobbyInfoDF = pd.DataFrame(lobbyInfoArr)

    motionDF, sessionDF, lapDataDF, eventDF, carSetupsDF, carTelemetryDF, carStatusDF = addColumnNames(motionDF,
    sessionDF, lapDataDF, eventDF, carSetupsDF, carTelemetryDF, carStatusDF)

    return motionDF, sessionDF, lapDataDF, eventDF, carSetupsDF, carTelemetryDF, carStatusDF

def Tables(motionDF, sessionDF, lapDataDF, eventDF, carSetupsDF, carTelemetryDF, carStatusDF, conn):
    motionDF.to_sql("motionData", con = conn, schema=None, if_exists='replace')
    lapDataDF.to_sql("LapData", con = conn, schema=None, if_exists='replace')
    eventDF.to_sql("EventData", con = conn, schema=None, if_exists='replace')
    carSetupsDF.to_sql("CarSetupData", con = conn, schema=None, if_exists='replace')
    carTelemetryDF.to_sql("TelemetryData", con = conn, schema=None, if_exists='replace')
    carStatusDF.to_sql("CarStatusData", con = conn, schema=None, if_exists='replace')

#getting master table
def masterLapData(connection):
    lapTimesDf = getLapTimes(connection)
    lapTimesDf = addNames(lapTimesDf)
    lapTimesDf = finalLapTime(lapTimesDf)
    masterLapDataDfVars = ["SessionTime", "lastLapTime", "currentLapTime", "bestLapTime", "currentLapNum", "finalLapTime"]
    masterLapDataDf = lapTimesDf[masterLapDataDfVars]
    return masterLapDataDf


def masterPacketData(connection):
    cur = connection.cursor()
    cur.execute("SELECT pkt_id, packetId, sessionUID, sessionTime FROM packets")
    masterPacketDf = pd.DataFrame(cur.fetchall())
    packetCols = ["pkt_id", "packetId", "sessionUID", "SessionTime"]
    masterPacketDf.columns = packetCols
    return masterPacketDf

def masterMotionData(connection):
    cur = connection.cursor()
    cur.execute("""SELECT SessionTime, worldPositionX, worldPositionY, worldPositionZ,
        worldVelocityX, worldVelocityY, worldVelocityZ, yaw, pitch, roll FROM motionData""")

    masterMotionDf = pd.DataFrame(cur.fetchall())
    motionCols = ["SessionTime", "worldPositionX", "worldPositionY", "worldPositionZ",
        "worldVelocityX", "worldVelocityY", "worldVelocityZ", "yaw", "pitch", "roll"]

    masterMotionDf.columns = motionCols
    return masterMotionDf

def masterTelemetryData(connection):
    cur = connection.cursor()
    cur.execute("""SELECT SessionTime, speed, throttle, steer, brake, clutch, gear, engineRPM,
     drs, brakesTemperatureRL, brakesTemperatureRR, brakesTemperatureFL, brakesTemperatureFR,
     tyresSurfaceTemperatureRL, tyresSurfaceTemperatureRR, tyresSurfaceTemperatureFL,
     tyresSurfaceTemperatureFR, engineTemperature FROM telemetryData""")
    masterTelemetryDf = pd.DataFrame(cur.fetchall())
    telemetryCols = ["SessionTime", "speed", "throttle", "steer", "brake", "clutch", "gear", "engineRPM",
    "drs", "brakesTemperatureRL", "brakesTemperatureRR", "brakesTemperatureFL", "brakesTemperatureFR",
    "tyresSurfaceTemperatureRL", "tyresSurfaceTemperatureRR",
    "tyresSurfaceTemperatureFL", "tyresSurfaceTemperatureFR", "engineTemperature"]
    masterTelemetryDf.columns = telemetryCols
    return masterTelemetryDf

def masterSetupData(connection):
    cur = connection.cursor()
    cur.execute("SELECT * FROM CarSetupData")
    masterSetupDF = pd.DataFrame(cur.fetchall())
    setupCols = ["Index", "SessionTime", "frontWing", "rearWing", "onThrottle", "offThrottle", "frontCamber",
    "rearCamber", "frontToe", "rearToe", "frontSuspension", "rearSuspension", "frontAntiRollBar",
    "rearAntiRollBar", "frontSuspensionHeight", "rearSuspensionHeight", "brakePressure", "brakeBias",
    "rearLeftTyrePressure", "rearRightTyrePressure", "frontLeftTyrePressure", "frontRightTyrePressure",
    "ballast","fuelLoad"]
    masterSetupDF.columns = setupCols
    masterSetupDF = masterSetupDF.drop('Index', 1)
    return masterSetupDF

def masterStatusData(connection):
    cur = connection.cursor()
    cur.execute("""SELECT sessionTime, fuelMix, FrontBrakeBias, fuelInTank, fuelRemainingLaps,
    tyresWearRL, tyresWearRR, tyresWearFL, tyresWearFR, actualTyreCompound, tyresAgeLaps  FROM carStatusData""")
    masterStatusDf = pd.DataFrame(cur.fetchall())
    statusCols = ["SessionTime", "fuelMix", "FrontBrakeBias", "fuelInTank", "fuelRemainingLaps",
    "tyresWearRL", "tyresWearRR", "tyresWearFL", "tyresWearFR", "actualTyreCompound", "tyresAgeLaps"]
    masterStatusDf.columns = statusCols
    return masterStatusDf


def masterData(conn):

    masterLapDf = masterLapData(conn)
    masterPacketDf = masterPacketData(conn)
    masterMotionDf = masterMotionData(conn)
    masterTelemetryDf = masterTelemetryData(conn)
    masterSetupDF = masterSetupData(conn)
    masterStatusDf = masterStatusData(conn)


    masterDf = masterLapDf.merge(masterPacketDf, on='SessionTime').merge(masterMotionDf, on='SessionTime').merge(masterTelemetryDf, on='SessionTime').merge(masterSetupDF, on='SessionTime').merge(masterStatusDf, on='SessionTime')

    return masterDf

def masterDfToSQL(df, conn):
    df.to_sql("MasterData", con = conn, schema = None, if_exists = 'replace')

def DBExpand(database):
    # try:
    column_names = ["pkt_id", "timestamp", "packetFormat", "gameMajorVersion", "gameMinorVersion", "packetVersion", "packetId", "sessionUID", "sessionTime", "frameIdentifier", "playerCarIndex", "packet"]
        #database = "SQL_files/F1_2020_51101ca1a9b0ff60.sqlite3" testing with this database
    conn = connect(database)
    df = selectALL(conn)
    df.columns = column_names
    df.reset_index(drop = True, inplace = True)
    motionDF, sessionDF, lapDataDF, eventDF, carSetupsDF, carTelemetryDF, carStatusDF = globalFormater(df)
    Tables(motionDF, sessionDF, lapDataDF, eventDF, carSetupsDF, carTelemetryDF, carStatusDF, conn)
    masterDf = masterData(conn)
    masterDfToSQL(masterDf, conn)
    conn.close()
    # except:
    #     logging.info("Error: Database does not exist")
