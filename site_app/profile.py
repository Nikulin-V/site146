#  Nikulin Vasily © 2021
from flask import render_template, redirect, request
from flask_login import login_required, current_user

from site_app import site
from data import db_session
from forms.profile import ProfileForm
from tools.tools import roles_allowed
from tools.url import url


@site.route('/profile', methods=['GET', 'POST'])
@login_required
@roles_allowed('user')
def profile():
    form = ProfileForm()
    db_sess = db_session.create_session()
    user = current_user

    message = ''

    if form.validate_on_submit():
        message = "Сохранено"

        user.surname = form.surname.data
        user.name = form.name.data
        user.patronymic = form.patronymic.data
        user.email = form.email.data

        if form.old_password.data or form.password.data or form.password_again.data:
            if not form.old_password.data:
                message = "Введите старый пароль"
            elif not form.password.data:
                message = "Введите новый пароль"
            elif not form.password_again.data:
                message = "Повторите новый пароль"
            elif not user.check_password(form.old_password.data):
                message = "Неверный старый пароль"
            elif form.password.data != form.password_again.data:
                message = "Пароли не совпадают"
            else:
                user.set_password(form.password.data)

        db_sess.merge(user)
        db_sess.commit()

        if request.args.get('redirect_page'):
            return redirect(url(request.args.get('redirect_page')))

    return render_template("site/profile.html",
                           title='Профиль',
                           form=form,
                           message=message)
