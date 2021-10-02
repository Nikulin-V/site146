#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy
from flask_security import RoleMixin
from sqlalchemy.orm import relationship

from data.db_session import SqlAlchemyBase


class Role(SqlAlchemyBase, RoleMixin):
    __tablename__ = 'roles'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)
    description = sqlalchemy.Column(sqlalchemy.String)

    def __str__(self):
        return self.name


class RolesUsers(SqlAlchemyBase, RoleMixin):
    __tablename__ = 'roles_users'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))
    user_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('users.id'))
    user = relationship('User')
    role_id = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('roles.id'))
    role = relationship('Role')

    def __str__(self):
        return self.role.name
