#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy

from .db_session import SqlAlchemyBase


class Teacher(SqlAlchemyBase):
    __tablename__ = 'teachers'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    patronymic = sqlalchemy.Column(sqlalchemy.String)
    subject = sqlalchemy.Column(sqlalchemy.String)
    photo = sqlalchemy.Column(sqlalchemy.BLOB)
    about = sqlalchemy.Column(sqlalchemy.Text)
