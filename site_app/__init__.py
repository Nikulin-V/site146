#  Nikulin Vasily © 2021
from flask import Blueprint

from .api import api, socket

site = Blueprint('site', __name__, template_folder='templates', static_folder='static',
                 static_url_path='/site/static')
site.register_blueprint(api)

from .index import index
from .error_page import error_handler, error_page
from .login import login, logout
from .profile import profile
from .register import register
from .feed import feed
from .teachers import teachers
