import requests

address = input()

if address=="" or address.count(" ")==len(address):
    print('Введите адрес!')
else:
    url = f"https://geocode-maps.yandex.ru/1.x/?apikey=b2f42f9a-efc2-4a51-b051-5dbd204fa768&geocode={address}&format=json"
    r = requests.get(url)
    print(r.status_code)
    geo_code = r.json()
    coordinates = geo_code['response']
    coordinates_1 = coordinates['GeoObjectCollection']
    coordinates_2 = coordinates_1['featureMember']
    coordinates_3 = coordinates_2[0]
    coordinates_4 = coordinates_3['GeoObject']
    coordinates_5 = coordinates_4['Point']
    coordinates_6 = coordinates_5['pos']
    coordinates_6_1 = coordinates_6.split()
    latitude = float(coordinates_6_1[0])
    longitude = float(coordinates_6_1[1])
    print(latitude, longitude)

