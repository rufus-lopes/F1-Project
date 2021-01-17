import tensorflow as tf
import numpy as np
import os
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dropout, LSTM
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as mse



#import data
dir = '../SQL_Data/constant_setup'
files = os.listdir(dir)
files = [f for f in files if f.endswith('.sqlite3')]
data = []
for f in files:
    path = os.path.join(dir, f)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM TrainingData')
    df = pd.DataFrame(cur.fetchall())
    data.append(df)

names = list(map(lambda x: x[0], cur.description))
df = pd.concat(data)
df.columns = names


#format training data

lab = df.pop('finalLapTime')
X, x, Y, y = train_test_split(df, lab, test_size=0.2)

# initialise and train model
model = LinearRegression()
model.fit(X, Y)
preds = model.predict(x)
print(mse(y, preds))
