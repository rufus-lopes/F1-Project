import sqlite3
import pandas as pd
import numpy as np

def averages(df, timeStep):
    '''takes in a dataframe and timeStep and returns the a dataframe
    of the rolling average over that timeStep '''
    roll = df.rolling(timeStep, min_periods=1).mean()#maybe needs some tweaking
    return roll

def sums(df):
    '''takes the averaged df as input and concatonates onto the side
    the cumulative sum of all variables'''

    sumDf = df.cumsum()
    return sumDf

def getMainDf(db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT * FROM MasterData")
    df = pd.DataFrame(cur.fetchall())
    names = list(map(lambda x: x[0], cur.description))
    df.columns = names
    df.set_index(names[0], inplace=True)
    names.pop(0)
    return df, names, conn

def groupByLaps(df):
    g = df.groupby('currentLapNum')
    groupNames = list(g.groups)
    data = []
    for n in groupNames:
        data.append(g.get_group(n))
    return data


def selectSumColumns(df, columnsToSum):
    '''selects appropriate columns to be summed'''
    df = df[columnsToSum]
    return df

def toSQL(df, conn):
    df.to_sql('TrainingData', con = conn, schema = None, if_exists = 'replace')

def trainingCalculations(db):

    columnsToSum = [
    'currentLapTime', 'worldPositionX', 'worldPositionY', 'worldPositionZ',
    'worldVelocityX', 'worldVelocityY', 'worldVelocityZ', 'yaw', 'pitch',
    'roll', 'speed', 'throttle', 'steer', 'brake', 'clutch', 'gear',
    'engineRPM', 'drs', "brakesTemperatureRL", "brakesTemperatureRR",
    "brakesTemperatureFL", "brakesTemperatureFR",  "tyresSurfaceTemperatureRL",
    "tyresSurfaceTemperatureRR", "tyresSurfaceTemperatureFL",
    "tyresSurfaceTemperatureFR", 'engineTemperature',
    "tyresWearRL", "tyresWearRR", "tyresWearFL", "tyresWearFR"
    ]

    df, names, conn = getMainDf(db)
    timeStep = 10 # currently measured in packets - can easily adjust from here
    data = groupByLaps(df)
    averagedData = []
    for d in data:
        averagedData.append(averages(d, timeStep))

    fullAveragedData = pd.concat(averagedData)
    fullAveragedData.drop(['pkt_id', 'packetId', 'sessionTime', 'frameIdentifier'], inplace=True)

    summedData = []
    for i in data:
        i = selectSumColumns(i, columnsToSum)
        summedData.append(sums(i))

    sumNames = columnsToSum
    for i in range(len(sumNames)):
        sumNames[i] = 'summed_' + sumNames[i]

    fullSummedData = pd.concat(summedData)
    fullSummedData.columns = sumNames

    finalData = pd.concat([fullAveragedData, fullSummedData], axis = 1, ignore_index=False)

    toSQL(finalData, conn)
