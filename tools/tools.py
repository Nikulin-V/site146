#  Nikulin Vasily © 2021
import functools
import os
import random
import string

import flask
from flask import request, jsonify, abort
from flask_login import current_user, AnonymousUserMixin
from flask_socketio import emit


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
