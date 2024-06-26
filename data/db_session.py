import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

SqlAlchemyBase = orm.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models
    from . import prediction
    from . import cards

    SqlAlchemyBase.metadata.create_all(engine)

    # запуск базы данных
    session = create_session()
    if session.query(prediction.Prediction).count() == 0:
        # формрование базы данных предсказаний
        prediction.init_prediction()
    if session.query(cards.Cards).count() == 0:
        # формрование базы данных карт
        cards.init_cards()


def create_session() -> Session:
    global __factory
    return __factory()
