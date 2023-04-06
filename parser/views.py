import requests
from django.shortcuts import render, HttpResponse
import pandas as pd

from parser.apps.apartment.Analyze import Analyze
from parser.apps.db.OlxApartment import OlxApartment

from parser.apps.apartment.RandomForest import RandomForest

from parser.apps.apartment.GradientBoostingClassifier import GradientBoosting

from parser.apps.apartment.OlxLinearRegression import OlxLinearRegression


def apartment(request):
    if request.method == 'POST':
        token = request.body.decode('utf-8')
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
        upload_file('http://192.168.0.106/api/getFiles', 'parser/apps/files/matrix.png', 'matrix', token)
        upload_file('http://192.168.0.106/api/getFiles', 'parser/apps/files/importance.json', 'importance', token)
        return HttpResponse({'status': 'ok'})
    else:
        return HttpResponse(status=405)


def upload_file(url, loc, name, token):
    file = open(loc, 'rb')
    requests.post(url, data={'name': name}, files={'file': file}, headers={"Authorization": f"Bearer {token}"})
    file.close()
