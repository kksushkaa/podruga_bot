import sqlite3
from pprint import pprint
drinks = sqlite3.connect("stars.db")
cursor = drinks.cursor()
# create bd
cursor.execute("""CREATE TABLE cafe_drink
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 cafe_name TEXT,
                 cafe_address TEXT,
                 path_image TEXT,
                 latitude DOUBLE,
                 longitude DOUBLE)

           """)

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
for product in cafe_drink:
    cursor.execute(f"INSERT INTO cafe_drink (cafe_name,cafe_address, path_image, latitude, longitude) VALUES ('{product[0]}', '{product[1]}', '{product[2]}', {product[3]}, {product[4]})")
drinks.commit()
# read from bd
cursor.execute("SELECT * FROM cafe_drink")
pprint(cursor.fetchall())
