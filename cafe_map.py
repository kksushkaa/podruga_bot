import requests
from pprint import pprint
# url = r"https://static-maps.yandex.ru/v1?ll=37.620070,55.753630&size=450,450&z=13&pt=37.620070,55.753630,pmwtm1~37.64,55.76363,pmwtm99&apikey=9d7592b8-29c0-4693-ba7b-ef2b24ff62b1"
# r = requests.get(url)
cafe_drink = [
    ["Stars Coffee", "ул, Преображенская пл., 8", "frappe.jpg", 37.712812, 55.794887],
    ["Stars Coffee", "ул. Долгоруковская 7", "frappe.jpg", 37.603541, 55.773849],
    ["Stars Coffee", "Садовая-Самотечная ул., 24/27", "frappe.jpg", 37.620474, 55.773241],
    ["Stars Coffee", "Проспект мира, 40", "lemonage.jpg", 37.63376, 55.780233],
    ["Stars Coffee", "Шереметьевская ул., 20", "lemonage.jpg", 37.618776, 55.803322],
    ["Stars Coffee", "Правды ул., 26", "lemonage.jpg", 37.584829, 55.790519],
    ["Stars Coffee", "ул. Арбат 39-41", "frappe.jpg",37.589581, 55.748741],
    ["Stars Coffee", "Правобережная ул., 1Б", "frappe.jpg", 37.450162, 55.881046],
    ["Stars Coffee", "Новый Арбат 11, стр. 1", "lemonage.jpg", 37.662093, 55.845855],
    ["Stars Coffee", "ул. Кулакова, 20 к1", "americano.jpg", 37.390514, 55.803479],
    ["Stars Coffee", "Щукинская ул, 42", "americano.jpg", 37.464571, 55.809474],
    ["Stars Coffee", "Бутырский Вал ул., 10", "americano.jpg", 37.586068, 55.778461],
    ["Stars Coffee", "Ходынский бульвар, 4", "americano.jpg", 37.531289, 55.790231],
    ["Stars Coffee", "ул. Гашека, 6", "raf.jpg", 37.590542, 55.768345],
    ["Stars Coffee", "Ленинградский проспект, 39 стр 79", "raf.jpg", 37.537847, 55.796931],
    ["Stars Coffee", "ул. Верхняя Красносельская, д. 3А", "raf.jpg", 37.665551, 55.785604],
    ["Stars Coffee", "Вятская ул., 27", "raf.jpg", 37.581936, 55.796192],
    ["Stars Coffee", "Щелковское ш., 75", "rafi.jpg", 37.80108, 55.810966],
    ["Stars Coffee", "Мичуринский пр., 3 корпус 1", "rafi.jpg", 37.512973, 55.70355],
    ["Stars Coffee", "пл. Киевского вокзала, 2", "rafi.jpg", 37.566072, 55.744637],
    ["Stars Coffee", "Новодмитровская 1, стр. 1", "rafi.jpg", 37.584972, 55.80653]


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
    for e in cafe_drink:
        vec = (e[3]-latitude)**2+(e[4]-longitude)**2
        vec1 = vec**0.5
        if vec1<min_range:
            min_range = vec1
            shop_data = e
    print(shop_data)
