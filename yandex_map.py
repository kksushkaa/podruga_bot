import requests
from pprint import pprint
# url = r"https://static-maps.yandex.ru/v1?ll=37.620070,55.753630&size=450,450&z=13&pt=37.620070,55.753630,pmwtm1~37.64,55.76363,pmwtm99&apikey=9d7592b8-29c0-4693-ba7b-ef2b24ff62b1"
# r = requests.get(url)
shop_products = [
    ["Золотое яблоко", "пр-т Мира, 211, корп. 2", "biodepo.jpg", 37.662093, 55.845855],
    ["Золотое яблоко", "Ленинградское шоссе, 16А стр 4", "caudalie.jpg", 37.497468, 55.823216],
    ["Золотое яблоко", "Пресненская наб., 2", "blemish_toner.jpg", 37.539742, 55.749162],
    ["Золотое яблоко", "ул. Ярцевская, 19", "elasticpore_elizavecca.jpg", 37.411014, 55.738596],
    ["Золотое яблоко", "23-й км, Киевское шоссе, д. 1", "fruida.jpg", 37.422036, 55.623788],
    ["Золотое яблоко", "Чонгарский бульвар, 7", "miss_dior.jpg", 37.612389, 55.651384],
    ["Золотое яблоко", "Трубная пл., 2", "naturasiberica_conditioner.jpg", 37.622333, 55.766491],
    ["Золотое яблоко", "Кутузовский проспект, 57", "neogen.jpg", 37.476169, 55.727932],
    ["Золотое яблоко", "пл. Киевского Вокзала, 2", "zielinski_blackvanilla.jpg", 37.566072, 55.744637],
    ["Золотое яблоко", "Ходынский б-р, 4", "erborian_bbcream.jpg", 37.531289, 55.790231],


]
# url= r"https://static-maps.yandex.ru/v1?lang=ru_RU&ll=37.63199,55.81039&spn=0.016457,0.00619&apikey=9d7592b8-29c0-4693-ba7b-ef2b24ff62b1"
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
    # print(latitude, longitude)
    min_range = 1000000000000000000
    shop_data =[]
    for e in shop_products:
        vec = (e[3]-latitude)**2+(e[4]-longitude)**2
        vec1 = vec**0.5
        if vec1<min_range:
            min_range = vec1
            shop_data = e
    print(shop_data)




    # url_2 = f"https://static-maps.yandex.ru/v1?lang=ru_RU&ll={first_coordinate},{second_coordinate}&spn=0.016457,0.00619&apikey=9d7592b8-29c0-4693-ba7b-ef2b24ff62b1"
    # image = requests.get(url_2)
    # pprint(image)
    # line = image.content
    # file = open('image.png', 'wb')
    # file.write(line)

# url = f"https://geocode-maps.yandex.ru/1.x/?apikey=b2f42f9a-efc2-4a51-b051-5dbd204fa768&geocode={adress}&format=json"
# r = requests.get(url)
# print(r.status_code)

# print(r.text)
# pprint(r.json())
# geo_code = r.json()
# coordinates = geo_code['response']
# coordinates_1 = coordinates['GeoObjectCollection']
# coordinates_2 = coordinates_1['featureMember']
# coordinates_3 = coordinates_2[0]
# coordinates_4  =coordinates_3['GeoObject']
# coordinates_5  =coordinates_4['Point']
# coordinates_6  =coordinates_5['pos']
# coordinates_6_1 = coordinates_6.split()
# first_coordinate = coordinates_6_1[0]
# second_coordinate = coordinates_6_1[1]
#
#
#
# url_2= f"https://static-maps.yandex.ru/v1?lang=ru_RU&ll={first_coordinate},{second_coordinate}&spn=0.016457,0.00619&apikey=9d7592b8-29c0-4693-ba7b-ef2b24ff62b1"
# image = requests.get(url_2)
# pprint(image)
# line = image.content
# file = open('image.png', 'wb')
# file.write(line)
#





