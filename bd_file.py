# coding=<utf-8>
import sqlite3
import csv

conn = sqlite3.connect('./gadalka.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS cards(
                            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "card_name" TEXT,
                            "image" TEXT,
                            "yes_no_pred" TEXT)''')
with open('table1.csv', newline ='') as csv_file:
    reader_object = csv.reader(csv_file, delimiter=';')
    for n, row in enumerate(reader_object):
        if n != 0:
            cur.execute(f'INSERT INTO cards VALUES(Null, "{row[1]}", "{row[2]}", "{row[3]}")')
            print(row)

cur.execute('''CREATE TABLE IF NOT EXISTS prediction(
                            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
                            "day" TEXT,
                            "love" TEXT,
                            "career" TEXT)''')
with open('table2.csv', newline ='') as csv_file:
    reader_object = csv.reader(csv_file, delimiter=';')
    for n, row in enumerate(reader_object):
        if n != 0:
            cur.execute(f'INSERT INTO prediction VALUES(Null, "{row[1]}", "{row[2]}", "{row[3]}")')
            print(row)


conn.commit()
conn.close()