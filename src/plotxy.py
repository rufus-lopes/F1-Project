import sqlite3
from matplotlib import pyplot as plt
def plot():
    database = "SQL_files/F1_2020_4fb57d92601437be.sqlite3"
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT worldPositionX_m, worldPositionZ_m FROM motionData")
    data = cur.fetchall()
    X = []
    Y = []
    for p in data:
        X.append(p[0])
        Y.append(p[1])
    plt.plot(X, Y)
    plt.show()

if __name__ == "__main__":
    plot()
