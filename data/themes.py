#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class Sector(SqlAlchemyBase):
    __tablename__ = 'sectors'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    title = sqlalchemy.Column(sqlalchemy.String, unique=True)

    def __str__(self):
        return self.title


class Theme(SqlAlchemyBase):
    __tablename__ = 'themes'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    title = sqlalchemy.Column(sqlalchemy.String, unique=True)
    editors_role_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("roles.id"))
    editors_role = relationship("Role")

    def __str__(self):
        return self.title
