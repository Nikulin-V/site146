#  Nikulin Vasily © 2021
import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy import MetaData
from sqlalchemy.orm import Session, scoped_session, sessionmaker

__factory = None

SqlAlchemyBase = dec.declarative_base()
metadata = MetaData()


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine, autoflush=False)

    db_session = scoped_session(sessionmaker(autoflush=False, bind=engine))

    # noinspection PyUnresolvedReferences
    from . import __all_models

    SqlAlchemyBase.query = db_session.query_property()
    metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    # noinspection PyCallingNonCallable
    return __factory()
