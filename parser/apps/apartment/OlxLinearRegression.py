from sklearn.linear_model import LinearRegression

from parser.apps.apartment.Olx import Olx


class OlxLinearRegression(Olx):
    def getData(self):
        df = self.data[['rooms', 'floor', 'etajnost', 'area', 'metro', 'shops', 'repair', 'service', 'loc', 'price']]
        X = df.iloc[:, :-1].values
        y = df.iloc[:, 9].values
        model = LinearRegression()
        model.fit(X, y)
        self.data['Predict'] = model.predict(X)
        return self.data[['id', 'Predict']]
