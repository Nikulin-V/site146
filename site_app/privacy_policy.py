#  Nikulin Vasily © 2021
from flask import render_template

from site_app import site


@site.route('/privacy-policy')
def privacy_policy():
    return render_template("site/privacy_policy.html",
                           title='Политика конфиденциальности')
