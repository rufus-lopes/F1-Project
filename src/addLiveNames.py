def addLiveNames(arr):

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

    names = [motionCols, sessionCols, lapDataCols, carSetupsCols, carTelemetryCols, carStatusCols]

    for i in range(len(arr)):
        if not arr[i].empty:
            arr[i].columns = names[i]
    return arr
