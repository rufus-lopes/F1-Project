import sqlite3
import pandas as pd
import numpy as np
import os


#currently producing a dataframe for each lap.
#could work if able to train a model that outputs single value based on whole DataFrame
#model would have to be able to predict final value based on half-full dataframe when in operation - is this possible?


os.chdir("SQL_Data")
conn = sqlite3.connect("F1_2020_1a3b7c8065834b0d.sqlite3")
cur = conn.cursor()
cur.execute("SELECT * FROM MasterData")
df = pd.DataFrame(cur.fetchall())
names = list(map(lambda x: x[0], cur.description))
df.columns = names
df.columns = df.columns.str.strip()
g = df.groupby("currentLapNum")
groupNames = list(g.groups)
lapData = []
for l in groupNames:
    lapData.append(g.get_group(l))

print(type(lapData[0]))
# db = sqlite3.connect("groupTest.db")
# conn2 = sqlite3.connect("groupTest.sqlite3")
# df.to_sql("group", con = conn2, schema = None, if_exists = 'replace' )
