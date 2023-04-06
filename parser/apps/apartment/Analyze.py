import seaborn as sns
from sklearn.cluster import KMeans
from parser.apps.apartment.Olx import Olx
import pandas as pd
from sklearn.ensemble import ExtraTreesClassifier


class Analyze(Olx):
    def __init__(self, data: object):
        super().__init__(data)

    def getMatrixAnalize(self):
        sns.set_theme(style="ticks")
        df = self.data[['rooms', 'floor', 'etajnost', 'area', 'price']]
        result = sns.pairplot(df, hue="price")
        result.figure.savefig('parser/apps/files/matrix.png')

    def getProfit(self):
        df = self.data[['rooms', 'floor', 'etajnost', 'area', 'price', 'loc']]
        kmeans = KMeans(n_clusters=2)
        kmeans.fit(df)
        self.data['labels'] = kmeans.predict(df)
        return self.data[['id', 'labels']]

    def getImpotenAttribut(self):
        selector = ExtraTreesClassifier()
        df = self.data[['rooms', 'floor', 'etajnost', 'price', 'loc', 'area', 'metro', 'repair', 'service', 'shops']]
        result = selector.fit(df[df.columns], df['price'])
        features_table = pd.DataFrame(result.feature_importances_, index=df.columns,
                                      columns=['importance'])
        result = features_table.sort_values(by='importance', ascending=False)
        result['importance'].to_json('parser/apps/files/importance.json')
