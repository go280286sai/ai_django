from parser.apps.apartment.Olx import Olx
import pandas as pd
from sklearn.cluster import AffinityPropagation


class PredictListApartment(Olx):
    def getData(self, array):
        df = self.data[['id', 'rooms', 'etajnost', 'price', 'loc']]
        df.dropna()
        data_predict = pd.DataFrame(data=[array], columns=['rooms', 'etajnost', 'price', 'loc'])
        data_predict['loc'] = self.coder.transform(data_predict['loc'])
        a = df['price'].quantile(0.25)
        b = df['price'].quantile(0.75)
        df = df[(df['price'] < b + 1.5 * (b - a)) & (df['price'] > a - 1.5 * (b - a))]
        a = df['etajnost'].quantile(0.25)
        b = df['etajnost'].quantile(0.75)
        df = df[(df['etajnost'] < b + 1.5 * (b - a)) & (df['etajnost'] > a - 1.5 * (b - a))]
        model = AffinityPropagation(random_state=2)
        model.fit(df.iloc[:, 1:])
        df['label'] = model.labels_
        data_predict['label'] = model.predict(data_predict)
        label = data_predict['label'].values[0]
        get_id = df[df['label'] == label]['id']
        get_id = get_id.reset_index(drop=True)
        get_array = []
        for i in range(0, len(get_id)):
            get_array.append(get_id.loc[i])
            get_array.append(',')
        return get_array
