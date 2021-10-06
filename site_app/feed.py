#  Nikulin Vasily © 2021
from flask import render_template
from flask_login import login_required

from data import db_session
from data.news import Theme
from site_app import site

db_sess = db_session.create_session()


@site.route('/feed/<string:theme_address>', methods=['GET', 'POST'])
@login_required
def feed(theme_address):
    theme = db_sess.query(Theme).filter(Theme.address == theme_address).first()
    return render_template("site/feed.html",
                           theme=theme.title,
                           title=theme.title)
