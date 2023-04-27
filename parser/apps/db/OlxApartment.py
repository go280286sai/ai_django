from django.db import connection


class OlxApartment():
    def getData(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT id, rooms, floor, etajnost, price, date, location, area, favorites " \
                "FROM olx_apartments")
            return cursor.fetchall()
    def setNewPrice(self, data):
        count = data.id.count()
        for i in range(0, count):
            with connection.cursor() as cursor:
                sql=f"UPDATE olx_apartments SET real_price = {data['Predict'][i]} WHERE id = {data['id'][i]}"
                cursor.execute(sql)
                connection.commit()
    def setLocationIndex(self, data):
        count = data.id.count()
        for i in range(0, count):
            with connection.cursor() as cursor:
                cursor.execute(
                    f"Update olx_apartments Set location_index = {int(data['predict'][i])} where id = {data['id'][i]}")
                connection.commit()


