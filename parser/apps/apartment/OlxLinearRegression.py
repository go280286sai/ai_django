from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

from parser.apps.apartment.Olx import Olx


class OlxLinearRegression(Olx):
    def getData(self):
        df = self.data[['rooms', 'floor', 'etajnost', 'area', 'loc', 'price']]
        X = df.iloc[:, :-1].values
        y = df.iloc[:, 5].values
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.6, random_state=42)
        model = LinearRegression()
        model.fit(X_train, y_train)
        y_predict = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_predict)
        self.data['Predict'] = model.predict(X)
        return [mae, self.data[['id', 'Predict']]]

