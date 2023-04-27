from datetime import datetime, timedelta

from sklearn.metrics import mean_absolute_error


from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier

from parser.apps.apartment.Olx import Olx


class RandomForestStart(Olx):
    def getData(self):
        model = RandomForestClassifier(n_estimators=10)
        today = datetime.now().date()
        new_day=today-timedelta(days=5)
        data_train=self.data[self.data['date']<new_day][['rooms', 'floor', 'etajnost', 'area', 'loc', 'price']]
        data_train=data_train.reset_index(drop=True)
        result = self.data[(self.data['date']>new_day) | (self.data['date']==new_day)][['rooms', 'floor', 'etajnost', 'area', 'loc', 'price', 'id']]
        result=result.reset_index(drop=True)
        data_test =result[['rooms', 'floor', 'etajnost', 'area', 'loc', 'price']]
        x = data_train.iloc[:, :-1].values
        y = data_train.iloc[:, 5].values
        x_2 = data_test.iloc[:, :-1].values
        model.fit(x, y)
        result['Predict'] = model.predict(x_2)
        mae = mean_absolute_error(result['price'], result['Predict'])
        return [mae, result[['id', 'Predict']]]