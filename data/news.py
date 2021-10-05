#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    sector_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('sectors.id'))
    sector = relationship("Sector")
    author_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String)
    message = sqlalchemy.Column(sqlalchemy.Text)
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    picture = sqlalchemy.Column(sqlalchemy.String)
    files_links = sqlalchemy.Column(sqlalchemy.String)
    liked_ids = sqlalchemy.Column(sqlalchemy.String)
