#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy
from sqlalchemy.orm import relationship

from .db_session import SqlAlchemyBase


class News(SqlAlchemyBase):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    theme_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('themes.id'))
    theme = relationship("Theme", primaryjoin="Theme.id == News.theme_id")
    author_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("users.id"))
    title = sqlalchemy.Column(sqlalchemy.String)
    message = sqlalchemy.Column(sqlalchemy.Text)
    date = sqlalchemy.Column(sqlalchemy.DateTime)
    picture = sqlalchemy.Column(sqlalchemy.String)
    files_links = sqlalchemy.Column(sqlalchemy.String)
    liked_ids = sqlalchemy.Column(sqlalchemy.String)


class Sector(SqlAlchemyBase):
    __tablename__ = 'sectors'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, default=lambda: str(uuid4()),
                              nullable=False)

    def __str__(self):
        return self.title


class Theme(SqlAlchemyBase):
    __tablename__ = 'themes'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    title = sqlalchemy.Column(sqlalchemy.String, default=lambda: str(uuid4()), nullable=False)
    address = sqlalchemy.Column(sqlalchemy.String, unique=True, default=lambda: str(uuid4()),
                                nullable=False)
    sector_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("sectors.id"))
    sector = relationship("Sector")
    editors_role_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("roles.id"))
    editors_role = relationship("Role", primaryjoin="Theme.editors_role_id == Role.id")
    viewers_role_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey("roles.id"))
    viewers_role = relationship("Role", primaryjoin="Theme.viewers_role_id == Role.id")

    def __str__(self):
        return self.title
