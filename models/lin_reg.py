import tensorflow as tf
import numpy as np
import os
import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae
import pickle

def import_training_data():
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
    df = df.drop(['frameIdentifier','bestLapTime', 'pkt_id', 'packetId', 'SessionTime'], axis=1)
    df.set_index('index', inplace=True)

    return df


def save_model(model):
    file_name = 'LinearRegression.pkl'
    pickle.dump(model, open(file_name, 'wb'))

#format training data
df = import_training_data()
labels = df.pop('finalLapTime')
print(df.info())
X, x, Y, y = train_test_split(df, labels, test_size=0.2)

# initialise and train model
model = LinearRegression()
model.fit(X, Y)
preds = model.predict(x)
save_model(model)
# evaluate predictions
print(mae(y, preds))
