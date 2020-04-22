import sys
import requests
from io import BytesIO


class MapOfToponym:
    def __init__(self, toponym, type_map="scheme", trf=False, type_marker="comma"):
        self.type_marker = type_marker
        self.toponym = self.get_toponym(toponym)
        self.trf = trf
        if not self.toponym:
            self.map = "Нет такого населенного пункта"
            return
        self.coordinates = self.get_coordinates()
        self.map = self.get_map(*self.get_coordinates(), self.get_spn(), type_map)

    def change_type_marker(self, type_marker):
        self.type_marker = type_marker

    def get_toponym(self, toponym_to_find):
        # Возвращает топоним по его названию
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": toponym_to_find,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            pass
        json_response = response.json()
        if json_response["response"]["GeoObjectCollection"]["featureMember"] == []:
            toponym = None
        else:
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]
        return toponym

    def get_coordinates(self):
        # возвращает координаты центра топонима
        toponym = self.toponym
        if not toponym:
            return (0, 0)
        toponym_coodrinates = toponym["Point"]["pos"]
        toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
        return toponym_longitude, toponym_lattitude

    def get_spn(self):
        # возвращает размер топонима
        if not self.toponym:
            return [0, 0]
        toponym = self.toponym["boundedBy"]
        spn1 = [float(x) for x in toponym["Envelope"]["lowerCorner"].split()]
        spn2 = [float(x) for x in toponym["Envelope"]["upperCorner"].split()]
        return [str((spn2[0] - spn1[0]) / 2), str((spn2[1] - spn1[1]) / 2)]

    def get_map(self, toponym_longitude, toponym_lattitude, spn, type_map):
        # возвращает поток байт, который ты сам сможешб потом преобразовать в картинку
        # все виды карт
        if not self.toponym:
            return "Нет такого населенного пункта"
        map_params = {
            "ll": ",".join([toponym_longitude, toponym_lattitude]),
            "spn": ",".join(spn),
        }
        if self.type_marker:
            map_params["pt"] = ",".join([*self.coordinates, self.type_marker])
        if type_map == "scheme":
            map_params["l"] = "map"
        elif type_map == "satellite":
            map_params["l"] = "sat"
        else:
            map_params["l"] = "sat,skl"
        if self.trf:
            map_params["l"] += ",trf"
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)
        return BytesIO(response.content)

    def get_result(self):
        return self.map
