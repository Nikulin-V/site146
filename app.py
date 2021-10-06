#  Nikulin Vasily © 2021
import os

import eventlet
from flask import Flask, Blueprint
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_mobility.mobility import Mobility
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy

import site_app
from config import SERVER_NAME, SCHEME
from data import db_session
from tools.scheduler import Scheduler
from tools.tools import get_header_structure
from tools.url import url

eventlet.monkey_patch()

app = Flask(__name__, subdomain_matching=True)
app.config.update(
    SERVER_NAME=SERVER_NAME,
    SECRET_KEY='area_secret_key',
    SQLALCHEMY_DATABASE_URI='sqlite:///db/database.sqlite',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SESSION_COOKIE_DOMAIN=SERVER_NAME,
    SESSION_COOKIE_HTTPONLY=False,
    MAX_CONTENT_LENGTH=32 * 1024 * 1024,
    PREFERRED_URL_SCHEME=SCHEME,
    MAIL_SERVER='smtp.yandex.ru',
    MAIL_PORT=465,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='no-reply@area-146.tk',
    MAIL_DEFAULT_SENDER='no-reply@area-146.tk',
    MAIL_PASSWORD='school146noreply'
)
app.config.from_pyfile('config-extended.py')

socket_ = SocketIO(app, cors_allowed_origins="*")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
scheduler = Scheduler()
mail = Mail(app)

Mobility(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.jinja_env.globals.update(url=url)
app.jinja_env.globals.update(header_structure=get_header_structure)
db_session.global_init('db/database.sqlite')


def main():
    port = int(os.environ.get('PORT', 80))
    socket_.run(app, host='0.0.0.0', port=port)


def add_admin_panel():
    admin_bp = Blueprint('admin-panel', __name__, url_prefix='/admin')
    app.register_blueprint(admin_bp, url_prefix="/admin")

    admin = Admin(app, base_template='admin/master-extended.html')
    from tools.admin import connect_models
    connect_models(admin)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    add_admin_panel()

    services = [site_app.site]
    for service in services:
        app.register_blueprint(service)

    sockets = [site_app.socket]
    for socket in sockets:
        socket_ = socket.init_io(socket_)

    from data.__all_models import *

    db.create_all()
    main()
