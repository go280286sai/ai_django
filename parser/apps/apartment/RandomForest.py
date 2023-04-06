from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import mean_absolute_error

from parser.apps.apartment.Olx import Olx


class RandomForest(Olx):
    def getData(self):
        model = RandomForestClassifier(max_depth=4, random_state=0)
        df_1 = self.data[self.data['favorites'] == 0][['rooms', 'floor', 'etajnost', 'area', 'metro', 'shops', 'repair', 'service', 'loc', 'price']]
        x = df_1.iloc[:, :-1].values
        y = df_1.iloc[:, 9].values
        df = self.data[['rooms', 'floor', 'etajnost', 'area', 'metro', 'shops', 'repair', 'service', 'loc', 'price']]
        x_2 = df.iloc[:, :-1].values
        model.fit(x, y)
        self.data['Predict'] = model.predict(x_2)
        mae = mean_absolute_error(self.data['price'], self.data['Predict'])
        return [mae, self.data[['id', 'Predict']]]
