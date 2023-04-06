from django.db import connection


class OlxApartment():
    def getData(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, rooms, floor, etajnost, price, date, location, area, metro, repair, service, shops, favorites " \
                "FROM olx_apartments")
            return cursor.fetchall()
    def setNewPrice(self, data):
        count = data.id.count()
        for i in range(0, count):
            with connection.cursor() as cursor:
                cursor.execute(f"Update olx_apartments Set real_price = {int(data['Predict'][i])} where id = {data['id'][i]}")
                connection.commit()
    def setLocationIndex(self, data):
        count = data.id.count()
        for i in range(0, count):
            with connection.cursor() as cursor:
                cursor.execute(
                    f"Update olx_apartments Set location_index = {int(data['labels'][i])} where id = {data['id'][i]}")
                connection.commit()


