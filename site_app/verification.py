#  Nikulin Vasily © 2021
from flask import render_template

from site_app import site


@site.route('/yandex_58762f224fa898fc.html')
def yandex_verification():
    return render_template('site/yandex_58762f224fa898fc.html')
