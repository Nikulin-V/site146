#  Nikulin Vasily © 2021
import jinja2.exceptions
from flask import render_template, abort

from data import db_session
from data.news import Theme
from site_app import site

db_sess = db_session.create_session()


@site.route('/feed/<string:theme_address>', methods=['GET', 'POST'])
def feed(theme_address):
    theme = db_sess.query(Theme).filter(Theme.address == theme_address).first()

    if theme.is_feed:
        return render_template("site/feed.html",
                               theme=theme.title,
                               title=theme.title)
    try:
        return render_template(f"site/{theme_address}.html",
                               theme=theme.title,
                               title=theme.title)
    except jinja2.exceptions.TemplateNotFound:
        return abort(404)
