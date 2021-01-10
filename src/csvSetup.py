import numpy as np
import pandas as pd
import csv
import logging
import socket
import os
from src.UDP_unpacker import unpackUDPpacket

def setupCSV(_sessionUID):
    sessionUID = _sessionUID
    parent = os.getcwd()
    dir = f"CSV_Data/{sessionUID}"
    _path = os.path.join(parent, dir)
    if not os.path.exists(_path):
        os.mkdir(_path)

    motionFileName = f"CSV_Data/{sessionUID}/motion.csv"
    sessionFileName = f"CSV_Data/{sessionUID}/session.csv"
    lapFileName = f"CSV_Data/{sessionUID}/lap.csv"
    eventFileName = f"CSV_Data/{sessionUID}/event.csv"
    setupFileName = f"CSV_Data/{sessionUID}/setup.csv"
    telemetryFileName = f"CSV_Data/{sessionUID}/telemetry.csv"
    statusFileName = f"CSV_Data/{sessionUID}/status.csv"

    fileNames = [motionFileName, sessionFileName, lapFileName, eventFileName, setupFileName, telemetryFileName, statusFileName]

    motionCols = ["frameIdentifier", "SessionTime", "worldPositionX", "worldPositionY", "worldPositionZ", "worldVelocityX", "worldVelocityY",
    "worldVelocityZ","worldForwardDirX", "worldForwardDirY", "worldForwardDirZ", "worldRightDirX", "worldRightDirY",
    "worldRightDirZ","gForceLateral", "gForceLongitudinal","gForceVertical", "yaw", "pitch", "roll", "suspensionPositionRL",
    "suspensionPositionRR", "suspensionPositionFL", "suspensionPositionFR", "suspensionVelocityRL",
    "suspensionVelocityRR", "suspensionVelocityFL", "suspensionVelocityFR", "suspensionAccelerationRL", "suspensionAccelerationRR",
    "suspensionAccelerationFL", "suspensionAccelerationFR", "wheelSpeedRL", "wheelSpeedRR", "wheelSpeedFL", "wheelSpeedFR", "wheelSlipRL",
    "wheelSlipRR", "wheelSlipFL","wheelSlipFR", "localVelocityX", "localVelocityY", "localVelocityZ", "angularVelocityX", "angularVelocityY",
    "angularVelocityZ", "angularAccelerationX", "angularAccelerationY", "angularAccelerationZ", "frontWheelsAngle"]

    sessionCols = ["frameIdentifier", "SessionTime", "Header", "weather", "trackTemperature", "airTemperature",
    "totalLaps", "trackLength", "sessionType", "trackId", "formula", "sessionTimeLeft",
     "sessionDuration", "pitSpeedLimit","gamePaused", "isSpectating", "spectatorCarIndex",
      "sliProNativeSupport", "numMarshalZones", "marshalZones", "safetyCarStatus",
       "networkGame", "numWeatherForecastSamples", "weatherForecastSamples"]

    lapDataCols = ["frameIdentifier", "SessionTime","lastLapTime", "currentLapTime", "sector1TimeInMS", "sector2TimeInMS", "bestLapTime",
    "bestLapNum", "bestLapSector1TimeInMS", "bestLapSector2TimeInMS", "bestLapSector3TimeInMS",
    "bestOverallSector1TimeInMS", "bestOverallSector1LapNum", "bestOverallSector2TimeInMS",
    "bestOverallSector2LapNum", "bestOverallSector3TimeInMS", "bestOverallSector3LapNum",
    "lapDistance", "totalDistance", "safetyCarDelta", "carPosition", "currentLapNum",
    "pitStatus", "sector", "currentLapInvalid", "penalties", "gridPosition", "driverStatus",
    "resultStatus"]

    eventCols = ["frameIdentifier", "SessionTime", "eventDetails"]

    carSetupsCols = ["frameIdentifier", "SessionTime", "frontWing", "rearWing", "onThrottle", "offThrottle", "frontCamber",
    "rearCamber", "frontToe", "rearToe", "frontSuspension", "rearSuspension", "frontAntiRollBar",
    "rearAntiRollBar", "frontSuspensionHeight", "rearSuspensionHeight", "brakePressure", "brakeBias",
    "rearLeftTyrePressure", "rearRightTyrePressure", "frontLeftTyrePressure", "frontRightTyrePressure",
    "ballast","fuelLoad"]

    carTelemetryCols = ["frameIdentifier", "SessionTime", "speed", "throttle", "steer", "brake", "clutch", "gear", "engineRPM",
     "drs", "revLightsPercent", "brakesTemperatureRL", "brakesTemperatureRR",
     "brakesTemperatureFL", "brakesTemperatureFR", "tyresSurfaceTemperatureRL", "tyresSurfaceTemperatureRR",
     "tyresSurfaceTemperatureFL", "tyresSurfaceTemperatureFR", "tyresInnerTemperatureRL",
     "tyresInnerTemperatureRR", "tyresInnerTemperatureFL", "tyresInnerTemperatureFR",
     "engineTemperature", "tyresPressureRL", "tyresPressureRR", "tyresPressureFL", "tyresPressureFR",
     "surfaceTypeRL", "surfaceTypeRR", "surfaceTypeFL", "surfaceTypeFR"]

    carStatusCols = ["frameIdentifier", "SessionTime", "tractionControl", "antiLockBrakes", "fuelMix", "frontBrakeBias",
    "pitLimiterStatus", "fuelInTank", "fuelCapacity", "fuelRemainingLaps", "maxRPM", "idleRPM", "maxGears",
    "drsAllowed", "drsActivationDistance", "tyresWearRL", "tyresWearRR", "tyresWearFL", "tyresWearFR",
    "actualTyreCompound", "visualTyreCompound", "tyresAgeLaps", "tyresDamageRL", "tyresDamageRR",
     "tyresDamageFL", "tyresDamageFR", "frontLeftWingDamage", "frontRightWingDamage", "rearWingDamage",
     "drsFault", "engineDamage", "gearBoxDamage", "vehicleFiaFlags", "ersStoreEnergy", "ersDeployMode",
     "ersHarvestedThisLapMGUK", "ersHarvestedThisLapMGUH", "ersDeployedThisLap"]

    columnNames = [motionCols, sessionCols, lapDataCols, eventCols, carSetupsCols, carTelemetryCols, carStatusCols]

    for i in range(len(columnNames)):
        file = fileNames[i]
        col = columnNames[i]
        with open(file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(col)

def getSessionInfo():
    """Captures the first packet of the session and uses this for basic information regarding
    visualiser setup"""

    UDP_IP = "0.0.0.0"
    UDP_PORT = 20777
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    logging.info("Waiting for session to start")
    while True:
        data, addr = sock.recvfrom(2048)
        if data:
            break

    return unpackUDPpacket(data)
