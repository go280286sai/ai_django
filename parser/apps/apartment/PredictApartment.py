import json

from sklearn.ensemble import RandomForestClassifier

from parser.apps.apartment.Olx import Olx
import pandas as pd


class PredictApartment(Olx):
    def getData(self, array):
        df = self.data[['rooms', 'floor', 'etajnost', 'area', 'loc', 'price']]
        data_predict = pd.DataFrame(data=[array], columns=['rooms', 'floor', 'etajnost', 'area', 'loc'])
        data_predict['loc'] = self.coder.transform(data_predict['loc'])
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
        result = model.predict(data_predict.iloc[:, :].values)
        return json.dumps({'result': int(result[0])})
