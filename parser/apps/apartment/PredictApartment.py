import json

from sklearn.ensemble import RandomForestClassifier

from parser.apps.apartment.Olx import Olx
import pandas as pd
from sklearn import preprocessing
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


class PredictApartment(Olx):
    def getData(self, array):
        df = self.data[['rooms', 'floor', 'etajnost', 'area', 'loc', 'price']]
        df.dropna()
        loc_predict = array[0][-1]
        array[0][-1] = self.data[self.data['location']==array[0][-1]]['loc'].unique()[0]
        a = df['price'].quantile(0.25)
        b = df['price'].quantile(0.75)
        df = df[(df['price'] < b + 1.5 * (b - a)) & (df['price'] > a - 1.5 * (b - a))]
        a = df['etajnost'].quantile(0.25)
        b = df['etajnost'].quantile(0.75)
        df = df[(df['etajnost'] < b + 1.5 * (b - a)) & (df['etajnost'] > a - 1.5 * (b - a))]
        X = df.iloc[:, :-1].values
        y = df.iloc[:, 5].values
        model = RandomForestClassifier(n_estimators=10)
        model.fit(X, y)
        result = []
        result = model.predict(array)
        return json.dumps({'result':int(result[0])})

