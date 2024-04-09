import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase, create_session
import csv


class Prediction(SqlAlchemyBase):
    __tablename__ = 'prediction'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    day = sqlalchemy.Column(sqlalchemy.String)
    love = sqlalchemy.Column(sqlalchemy.String)
    career = sqlalchemy.Column(sqlalchemy.String)


def init_prediction():
    session = create_session()
    with open('table2.csv', newline='') as csv_file:
        reader_object = csv.reader(csv_file, delimiter=';')
        for n, row in enumerate(reader_object):
            if n != 0:
                new_prediction = Prediction(day=row[1], love=row[2], career=row[3])
                print(row)
                session.add(new_prediction)
    session.commit()
    session.close()

if __name__ == '__main__':
    init_prediction()
