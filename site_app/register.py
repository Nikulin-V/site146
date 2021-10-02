#  Nikulin Vasily © 2021
from flask import redirect, render_template, request
from flask_login import current_user, login_user

from site_app import site
from data import db_session
from data.users import User
from forms.register import RegisterForm
from tools.url import url


@site.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect('/profile')

    db_sess = db_session.create_session()

    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template("site/register.html",
                                   title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают",
                                   btn_label='Войти')

        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template("site/register.html",
                                   title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть",
                                   btn_label='Войти')

        # noinspection PyArgumentList
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
        )

        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        user.add_roles(['user'])

        login_user(user)

        return redirect(url(request.args.get('redirect_page') or ".profile"))

    return render_template("site/register.html",
                           title='Регистрация',
                           form=form,
                           btn_label='Войти')
