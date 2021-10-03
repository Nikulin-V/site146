#  Nikulin Vasily © 2021
from flask import redirect, render_template, request
from flask_login import current_user, login_user, login_required, logout_user

from site_app import site, socket
from data import db_session
from data.users import User
from forms.login import LoginForm
from tools.tools import send_response
from tools.url import url


@socket.on('login')
@site.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url('.profile'))

    form = LoginForm()

    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user: User
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if not user:
            return send_response('loginError', {
                'message': 'Error',
                'errors': ["Вы не зарегистрированы в системе"]
            })
        if user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            redirect_page = request.args.get('redirect_page')
            redirect_page = 'admin.index' if redirect_page == 'site.error_page' else redirect_page
            return redirect(url(redirect_page or ".index"))
        return send_response('loginError', {
            'message': 'Error',
            'errors': ["Неверный логин или пароль"]
        })
    return render_template("site/login.html",
                           title='Авторизация',
                           form=form)


@site.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url('site.login'))
