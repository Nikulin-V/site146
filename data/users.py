#  Nikulin Vasily © 2021
from uuid import uuid4

import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db_session
from .db_session import SqlAlchemyBase
from .roles import RolesUsers, Role


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True, default=lambda: str(uuid4()))

    surname = sqlalchemy.Column(sqlalchemy.String)
    name = sqlalchemy.Column(sqlalchemy.String)
    patronymic = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)

    def has_role(self, role_name):
        db_sess = db_session.create_session()
        for role_id in db_sess.query(RolesUsers.role_id).filter(
                RolesUsers.user_id == self.id).all():
            if db_sess.query(Role).get(role_id).name == role_name:
                return True
        return False

    def add_roles(self, roles):
        if 'user' not in roles and not self.has_role('user'):
            roles.append('user')
        db_sess = db_session.create_session()
        for role_name in roles:
            if not self.has_role(role_name):
                role = RolesUsers(
                    user_id=self.id,
                    role_id=db_sess.query(Role.id).filter(Role.name == role_name)
                )
                db_sess.add(role)
        db_sess.commit()

    def clear_roles(self, roles=None):
        db_sess = db_session.create_session()
        if roles is None:
            roles = db_sess.query(RolesUsers).filter(RolesUsers.user_id == self.id).all()
        else:
            roles_ids = list(map(lambda x: x[0],
                                 db_sess.query(Role.id).filter(Role.name.in_(roles)).all()))
            roles = db_sess.query(RolesUsers).filter(RolesUsers.user_id == self.id,
                                                     RolesUsers.role_id.in_(roles_ids)).all()
        for role_user in roles:
            db_sess.delete(role_user)
        db_sess.commit()

    def set_roles(self, roles):
        self.clear_roles()
        self.add_roles(roles)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __str__(self):
        return f'{self.surname} {self.name} | {self.email}'
