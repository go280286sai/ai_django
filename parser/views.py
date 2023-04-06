from django.shortcuts import render, HttpResponse
from django.db import connection
import pandas as pd

from parser.apps.apartment.Analyze import Analyze
from parser.apps.db.OlxApartment import OlxApartment

from parser.apps.apartment.RandomForest import RandomForest

from parser.apps.apartment.GradientBoostingClassifier import GradientBoosting

from parser.apps.apartment.OlxLinearRegression import OlxLinearRegression


def apartment(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        data = pd.DataFrame(OlxApartment().getData(),
                            columns=['id', 'rooms', 'floor', 'etajnost', 'price', 'date', 'location', 'area', 'metro',
                                     'repair',
                                     'service', 'shops', 'favorites'])
        if (data['id'].count() * 0.3 <= data[data['favorites'] == 0]['id'].count()):
            send_data = OlxLinearRegression(data)
            OlxApartment().setNewPrice(send_data.getData())
        else:
            send_data_1 = RandomForest(data).getData()
            send_data_2 = GradientBoosting(data).getData()
            if (send_data_1[0] > send_data_2[0]):
                OlxApartment().setNewPrice(send_data_2[1])
            else:
                OlxApartment().setNewPrice(send_data_1[1])
        analitica = Analyze(data)
        analitica.getImpotenAttribut()
        analitica.getMatrixAnalize()
        OlxApartment().setLocationIndex(analitica.getProfit())
        return HttpResponse(request.POST.get('token'))
    else:
        return HttpResponse(status=405)




