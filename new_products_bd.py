import sqlite3
from pprint import pprint
products = sqlite3.connect("new_product.db")
cursor = products.cursor()
# create bd
cursor.execute("""CREATE TABLE shop_products
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 shop_name TEXT,
                 shop_address TEXT,
                 path_image TEXT,
                 latitude DOUBLE,
                 longitude DOUBLE)
                 
           """)

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
for product in shop_products:
    cursor.execute(f"INSERT INTO shop_products (shop_name,shop_address, path_image, latitude, longitude) VALUES ('{product[0]}', '{product[1]}', '{product[2]}', {product[3]}, {product[4]})")
products.commit()
# read from bd
cursor.execute("SELECT * FROM shop_products")
pprint(cursor.fetchall())
