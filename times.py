import sqlite3
import numpy as np
import pandas as pd

def connect(DBname):
    conn = sqlite3.connect(DBname)
    return conn

def getLapTimes(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM LapData")
    lapTimes = pd.DataFrame(cur.fetchall())
    return lapTimes

def addNames(df):
    lapDataCols = ["index", "SessionTime_s","lastLapTime", "currentLapTime", "sector1TimeInMS", "sector2TimeInMS", "bestLapTime",
    "bestLapNum", "bestLapSector1TimeInMS", "bestLapSector2TimeInMS", "bestLapSector3TimeInMS",
    "bestOverallSector1TimeInMS", "bestOverallSector1LapNum", "bestOverallSector2TimeInMS",
    "bestOverallSector2LapNum", "bestOverallSector3TimeInMS", "bestOverallSector3LapNum",
    "lapDistance", "totalDistance", "safetyCarDelta", "carPosition", "currentLapNum",
    "pitStatus", "sector", "currentLapInvalid", "penalties", "gridPosition", "driverStatus",
    "resultStatus"]

    df.columns = lapDataCols
    return df

def finalLapTime(df):
    lapNums = df['currentLapNum']
    lapTimes = df['currentLapTime']
    newLapIndex = []
    for i in range(len(lapNums)-1):
        currentLap = lapNums[i]
        nextLap = lapNums[i+1]
        if currentLap != nextLap:
            newLapIndex.append(i)
    newLapIndex.append(i)
    finalLapTimes = {lap:time for (lap,time) in zip(lapNums[newLapIndex],lapTimes[newLapIndex])}
    df['finalLapTime'] = [finalLapTimes[lap] for lap in lapNums]
    return df

def main():
    db = "SQL_Data/F1_2020_19ded668360606ef.sqlite3"
    connection = connect(db)
    lapTimesDf = getLapTimes(connection)
    lapTimesDf = addNames(lapTimesDf)
    lapTimesDf = lapTimesDf.reset_index(drop=True)
    print(finalLapTime(lapTimesDf).tail())

if __name__ == "__main__":
    main()