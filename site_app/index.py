#  Nikulin Vasily © 2021
from flask import render_template

from site_app import site


@site.route('/')
@site.route('/index')
def index():
    return render_template("site/index.html",
                           title='Главная')
