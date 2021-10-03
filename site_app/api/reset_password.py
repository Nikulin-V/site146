#  Nikulin Vasily © 2021
from flask_mail import Message

from app import mail
from data import db_session
from data.users import User
from site_app.api import api, socket
from tools.tools import fillJson, send_response, generate_random_string


@socket.on('sendCode')
@api.route('/api/users/reset', methods=['PUT'])
def reset_password(json=None):
    if json is None:
        json = dict()

    event_name = 'sendCode'
    fillJson(json, ['email'])

    email = json['email']

    db_sess = db_session.create_session()

    if email:
        user = db_sess.query(User).filter(
            User.email == email
        ).first()

    if not user:
        return send_response(
            event_name,
            {
                'message': 'Error',
                'errors': [f'The user with <email:{email}> not found']
            }
        )

    new_password = generate_random_string(8)
    user.set_password(new_password)

    msg = Message(subject='Сброс пароля на сайте школы №146',
                  body=f'Новый пароль: {new_password}\n'
                       f'Не забудьте поменять его после авторизации',
                  sender='support@area-146.tk',
                  recipients=[email])
    mail.send(msg)

    db_sess.merge(user)
    db_sess.commit()

    return send_response(
        event_name,
        {
            'message': 'Success',
            'errors': []
        }
    )
