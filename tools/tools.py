#  Nikulin Vasily © 2021
import functools
import os
import random
import string
from typing import Union

import flask
from flask import request, jsonify, abort
from flask_login import current_user, AnonymousUserMixin
from flask_socketio import emit

from data import db_session
from data.news import Sector, Theme
from data.teachers import Teacher


def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def fillJson(json, args):
    for arg in args:
        if arg not in json.keys():
            json[arg] = request.args.get(arg)


def send_response(event_name, response=None, *args, **kwargs):
    if hasattr(flask.request, 'namespace'):
        if response is None:
            emit(event_name, *args, **kwargs)
        else:
            emit(event_name, response, *args, **kwargs)
    else:
        return jsonify(response)


def safe_remove(file):
    if os.path.exists(file):
        os.remove(file)
        return True
    return False


def roles_required(*roles):
    def decorator(func):
        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            if isinstance(current_user, AnonymousUserMixin):
                return abort(401)
            if all([current_user.has_role(role)] for role in roles):
                return func(*args, **kwargs)
            return abort(403)

        return decorated_view

    return decorator


def roles_allowed(*roles):
    def decorator(func):
        @functools.wraps(func)
        def decorated_view(*args, **kwargs):
            if isinstance(current_user, AnonymousUserMixin):
                return abort(401)
            if any([current_user.has_role(role)] for role in roles):
                return func(*args, **kwargs)
            return abort(403)

        return decorated_view

    return decorator


def get_header_structure():
    db_sess = db_session.create_session()
    structure = {}
    sectors = db_sess.query(Sector).all()
    for sector in sectors:
        themes = db_sess.query(Theme).filter(Theme.sector_id == sector.id).all()
        themes = list(filter(has_view_permission, themes))
        if themes:
            structure[sector.title] = [(theme.title, theme.address)
                                       for theme in themes]
    return structure


def has_view_permission(theme: Union[Theme, str]):
    if isinstance(theme, str):
        db_sess = db_session.create_session()
        theme = db_sess.query(Theme).filter(Theme.title == theme).first()

    if not theme.viewers_role:
        return True
    if isinstance(current_user, AnonymousUserMixin):
        return False

    return current_user.has_role(theme.viewers_role.name)


def has_edit_permission(theme: Union[Theme, str]):
    if isinstance(theme, str):
        db_sess = db_session.create_session()
        theme = db_sess.query(Theme).filter(Theme.title == theme).first()

    if not theme.editors_role:
        return True
    if isinstance(current_user, AnonymousUserMixin):
        return False

    return current_user.has_role(theme.editors_role.name)


def update_teachers_images():
    db_sess = db_session.create_session()

    for teacher in db_sess.query(Teacher).all():
        if teacher.photo is not None:
            name = f'static/images/teachers/{teacher.id}.png'
            f = open(name, 'wb')
            f.write(teacher.photo)
            f.close()
