import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans
from parser.apps.apartment.Olx import Olx
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class Analyze(Olx):
    def __init__(self, data: object):
        super().__init__(data)

    def getMatrixAnalize(self):
        sns.set_theme(style="ticks")
        df = self.data[['rooms', 'floor', 'etajnost', 'area', 'price']]
        result = sns.pairplot(df, hue="price")
        result.figure.savefig('parser/apps/files/matrix.png')

    def getProfit(self):
        model = RandomForestClassifier(n_estimators=10)
        today = datetime.now().date()
        new_day = today - timedelta(days=5)
        data_train = self.data[self.data['date'] < new_day][
            ['rooms', 'floor', 'etajnost', 'area', 'loc', 'price', 'favorites']]
        data_train = data_train.reset_index(drop=True)
        result = self.data[(self.data['date'] > new_day) | (self.data['date'] == new_day)][
            ['rooms', 'floor', 'etajnost', 'area', 'loc', 'price', 'id', 'favorites']]
        result = result.reset_index(drop=True)
        data_test = result[['rooms', 'floor', 'etajnost', 'area', 'loc', 'price', 'favorites']]
        x = data_train.iloc[:, :-1].values
        y = data_train.iloc[:, 6].values
        x_2 = data_test.iloc[:, :-1].values
        model.fit(x, y)
        result['predict'] = model.predict(x_2)
        return result[['id', 'predict']]

    def getImpotenAttribut(self):
        selector = ExtraTreesClassifier()
        df = self.data[['rooms', 'floor', 'etajnost', 'price', 'loc', 'area']]
        result = selector.fit(df[df.columns], df['price'])
        features_table = pd.DataFrame(result.feature_importances_, index=df.columns,
                                      columns=['importance'])
        result = features_table.sort_values(by='importance', ascending=False)
        plt.style.use('_mpl-gallery-nogrid')
        # make data
        x = result['importance']

        labels = x.index.tolist()
        sizes = x.values.tolist()

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%',
               pctdistance=1.25, labeldistance=.6)

        plt.savefig('parser/apps/files/importance.png', dpi=300, bbox_inches='tight')
