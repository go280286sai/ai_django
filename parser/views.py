import json

import requests
from django.shortcuts import render, HttpResponse
import pandas as pd

from parser.apps.apartment.Analyze import Analyze
from parser.apps.apartment.PredictApartment import PredictApartment
from parser.apps.apartment.PredictListApartment import PredictListApartment
from parser.apps.db.OlxApartment import OlxApartment

from parser.apps.apartment.RandomForest import RandomForest


from parser.apps.apartment.OlxLinearRegression import OlxLinearRegression


def apartment(request):
    global mae
    if request.method == 'POST':
        token = request.body.decode('utf-8')
        data = pd.DataFrame(OlxApartment().getData(),
                            columns=['id', 'rooms', 'floor', 'etajnost', 'price', 'date', 'location', 'area', 'favorites'])
        if (data['id'].count() * 0.3 <= data[data['favorites'] == 0]['id'].count()):
            send_data = OlxLinearRegression(data).getData()
            OlxApartment().setNewPrice(send_data[1])
            mae = {'MAE': int(send_data[0])}
        else:
            send_data = RandomForest(data).getData()
            OlxApartment().setNewPrice(send_data[1])
            mae = {'MAE': int(send_data[0])}
        analitica = Analyze(data)
        analitica.getImpotenAttribut()
        analitica.getMatrixAnalize()
        OlxApartment().setLocationIndex(analitica.getProfit())
        upload_file('http://192.168.0.106/api/getFiles', 'parser/apps/files/matrix.png', 'matrix', token)
        upload_file('http://192.168.0.106/api/getFiles', 'parser/apps/files/importance.png', 'importance', token)
        return HttpResponse(json.dumps(mae), content_type='application/json')
    else:
        return HttpResponse(status=405)

def predictApartment(request):
    get_data=request.body.decode('utf-8')
    get_body=json.loads(get_data)
    if request.method == 'POST':
        data = pd.DataFrame(OlxApartment().getData(),
                            columns=['id', 'rooms', 'floor', 'etajnost', 'price', 'date', 'location', 'area',
                                     'favorites'])
        obj = PredictApartment(data)
        rooms = get_body['rooms']
        floor = get_body['floor']
        etajnost = get_body['etajnost']
        area = get_body['area']
        location = get_body['location']
        result = obj.getData([int(rooms), int(floor), int(etajnost), int(area), location])
        return HttpResponse(result)
    else:
        return HttpResponse(status=405)


def upload_file(url, loc, name, token):
    file = open(loc, 'rb')
    requests.post(url, data={'name': name}, files={'file': file}, headers={"Authorization": f"Bearer {token}"})
    file.close()


def getPredict(request):
    if request.method == 'POST':
        get_data = request.body.decode('utf-8')
        get_body = json.loads(get_data)
        rooms = get_body['rooms']
        etajnost = get_body['etajnost']
        price = get_body['price']
        location = get_body['location']
        data = pd.DataFrame(OlxApartment().getData(),
                           columns=['id', 'rooms', 'floor', 'etajnost', 'price', 'date', 'location', 'area',
                                    'favorites'])
        result=PredictListApartment(data).getData([rooms, etajnost, price, location])

        return HttpResponse(result)
    else:
        return HttpResponse(status=405)