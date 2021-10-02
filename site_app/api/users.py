#  Nikulin Vasily © 2021
from flask_login import login_required, current_user

from site_app.api import api, socket
from data import db_session
from data.users import User
from tools.tools import fillJson, send_response


@socket.on('getUsers')
@api.route('/api/users', methods=['GET'])
def getUsers(json=None):
    """
    Get info about user/users

    Required arguments: -

    Args:
        json (dict of str): user id or email

    JSON Args:
        identifier (str): user's id
        email (str): user's email

    Returns:
        Info about user/users (JSON)
    """

    if json is None:
        json = dict()

    event_name = 'getUsers'
    fillJson(json, ['identifier', 'email'])

    identifier = json['identifier']
    email = json['email']

    db_sess = db_session.create_session()

    if identifier:
        users = [db_sess.query(User).get(identifier)]
    elif email:
        users = db_sess.query(User).filter(
            User.email == email
        ).first()
    else:
        users = db_sess.query(User).all()

    if not users:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': [f'The user with <id:{identifier}> not found']
            }
        )

    return send_response(
        event_name,
        {
            'message': 'Success',
            'users':
                [item.to_dict(only=('id', 'surname', 'name', 'patronymic', 'email'))
                 for item in users]
        }
    )


# noinspection PyArgumentList
@socket.on('createUser')
@api.route('/api/users', methods=['POST'])
def createUser(json=None):
    """
    Create new user

    Required arguments:
        surname (string) - surname\n
        name (string) - name\n
        email (string) - email\n
        password (string) - password\n

    JSON Args:
        user_data (dict): dict of new user data

    User data:
        surname (string) - surname\n
        name (string) - name\n
        patronymic (string) - patronymic\n
        email (string) - email\n
        password (string) - password\n

    Returns:
        New user's id (JSON)
    """

    if json is None:
        json = dict()

    event_name = 'createUser'
    keys = ['surname', 'name', 'patronymic', 'email', 'password', 'roles']
    fillJson(json, keys)

    user_data = dict()
    for arg in json.keys():
        user_data[arg] = json[arg]

    db_sess = db_session.create_session()

    emails = db_sess.query(User.email).all()
    if user_data['email'] in emails:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['This email has already registered']
            }
        )

    user = User(
        surname=user_data['surname'],
        name=user_data['name'],
        patronymic=user_data['patronymic'],
        email=user_data['email']
    )
    user.set_password(user_data['password'])

    db_sess.add(user)
    db_sess.commit()

    user.add_roles(user_data['roles'])

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )


@socket.on('editUser')
@api.route('/api/users', methods=['PUT'])
@login_required
def editUser(json=None):
    if json is None:
        json = dict()

    event_name = 'editUser'
    fillJson(json, ['sessionId'])

    db_sess = db_session.create_session()
    user = db_sess.query(User).get(current_user.id)
    user.game_session_id = json['sessionId'] or current_user.game_session_id
    db_sess.merge(user)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )


@socket.on('deleteUser')
@api.route('/api/users', methods=['DELETE'])
@login_required
def deleteUser(json=None):
    """
    Delete user

    Required arguments:
        identifier (int) - user id\n
        email (string) - user email

    JSON Args:
        identifier (int): user id
        email (string): user email

    Returns:
        Success message (JSON)
    """

    if json is None:
        json = dict()

    event_name = 'deleteUser'
    fillJson(json, ['identifier', 'email'])

    identifier = json['identifier']
    email = json['email']

    if not (current_user.email == 'nikulin.vasily.777@ya.ru' or
            identifier == current_user.id or
            email == current_user.email):
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You do not have permissions to do this action']
            }
        )

    db_sess = db_session.create_session()

    if identifier is not None:
        user = db_sess.query(User).get(identifier)
    elif email is not None:
        user = db_sess.query(User).filter(User.email == email).first()
    else:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['You need to specify identifier or email']
            }
        )

    if user is None:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': ['User not found']
            }
        )

    db_sess.delete(user)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )
