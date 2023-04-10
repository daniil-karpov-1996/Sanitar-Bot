import requests
import os


def object_find(city, name_object):
    city_request = "http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" + city + "&format=json"
    city_response = requests.get(city_request).json()
    city_coord = city_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
    coord = city_coord.split()
    string_coord = coord[0] + "," + coord[1]
    object_request = "https://search-maps.yandex.ru/v1/?text=" + name_object + "&type=biz&lang=ru_RU&ll=" + string_coord + "&spn=1,1&results=100&apikey=6633a817-a99a-4d17-b557-a77557303ccc"
    object_response = requests.get(object_request)
    json_response = object_response.json()
    map_request = "https://static-maps.yandex.ru/1.x/?ll=" + string_coord + "&spn=0.05,0.05&l=map,skl&pt="
    for i in json_response['features']:
        coord_object = i['geometry']['coordinates']
        map_request += str(coord_object[0]) + "," + str(coord_object[1]) + ",pm2rdl" + "~"
    map_request = map_request[:-1]
    map_response = requests.get(map_request)
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(map_response.content)


city = input()
place = input()
object_find(city, place)
