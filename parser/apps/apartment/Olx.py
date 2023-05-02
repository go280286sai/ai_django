from sklearn import preprocessing


class Olx:
    def __init__(self, data: object):
        self.data = data
        self.coder = preprocessing.LabelEncoder()
        self.coder.fit(self.data['location'])
        self.data['loc'] = self.coder.transform(self.data['location'])
