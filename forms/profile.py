#  Nikulin Vasily © 2021
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, DateField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class ProfileForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    patronymic = StringField('Отчество')
    email = EmailField('Почта', validators=[DataRequired()])
    role = SelectField('Роль', validators=[DataRequired()],
                       choices=['Ученик', 'Учитель', 'Родитель'])
    old_password = PasswordField('Старый пароль')
    password = PasswordField('Пароль')
    password_again = PasswordField('Повторите пароль')
    submit = SubmitField()
