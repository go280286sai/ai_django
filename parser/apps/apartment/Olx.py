import numpy as np
import pandas as pd
from sklearn import preprocessing


class Olx:
    def __init__(self, data: object):
        self.data = data
        coder = preprocessing.LabelEncoder()
        coder.fit(self.data['location'])
        self.data['loc'] = coder.transform(self.data['location'])
