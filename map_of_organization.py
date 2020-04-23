import sys
import requests
from io import BytesIO


class MapOfOrganization:
    def __init__(self, toponym, type_map="scheme"):
        self.type_map = type_map
        self.toponym = self.get_toponym(toponym)
        if not self.toponym:
            self.map = "Нет такой организации"
        self.map = self.get_map()

    def get_toponym(self, toponym_to_find):
        # Возвращает топоним по его названию
        geocoder_api_server = "https://search-maps.yandex.ru/v1/"
        geocoder_params = {
            "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
            "text": toponym_to_find,
            "lang": "ru_RU",
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        if not response:
            return
        json_response = response.json()
        organizations = json_response["features"]
        return organizations

    def get_ll(self):
        toponym = self.toponym[0]
        return toponym["geometry"]["coordinates"]

    def get_map(self):
        try:
            type_map = self.type_map
            pt = []
            min_x = max_x = self.toponym[0]["geometry"]["coordinates"][0]
            min_y = max_y = self.toponym[0]["geometry"]["coordinates"][1]
            for i in self.toponym:
                point = i["geometry"]["coordinates"]
                org_name = i["properties"]["CompanyMetaData"]["name"]
                x = f"{point[0]},{point[1]},flag"
                pt.append(x)
                if point[0] > max_x:
                    max_x = point[0]
                if point[0] < min_x:
                    min_x = point[0]
                if point[1] > max_y:
                    max_y = point[1]
                if point[1] < min_y:
                    min_y = point[1]
            pt = "~".join(pt)
            spn = f"{(max_x - min_x)},{(max_y - min_y)}"
            x = str((max_x + min_x) / 2)
            y = str((max_y + min_y) / 2)
            map_params = {
                "ll": ",".join([x, y]),
                "spn" : spn,
                "pt" : pt
                }
            if type_map == "scheme":
                map_params["l"] = "map"
            elif type_map == "satellite":
                map_params["l"] = "sat"
            else:
                map_params["l"] = "sat,skl"
            map_api_server = "http://static-maps.yandex.ru/1.x/"
            response = requests.get(map_api_server, params=map_params)
            return BytesIO(response.content)
        except:
            return "что то пошло не так"

    def get_result(self):
        return self.map
