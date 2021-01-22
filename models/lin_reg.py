
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae
import pickle
from import_data import import_training_data
from sklearn.preprocessing import StandardScaler


def save_model(model):
    file_name = 'LinearRegression.pkl'
    pickle.dump(model, open(file_name, 'wb'))

#format training data
df = import_training_data()
labels = df.pop('finalLapTime')
X, x, Y, y = train_test_split(df, labels, test_size=0.2, random_state=42)

# initialise and train model
model = LinearRegression()
model.fit(X, Y)
preds = model.predict(x)
save_model(model)

# evaluate predictions
print(mae(y, preds))
print(preds[:5])
