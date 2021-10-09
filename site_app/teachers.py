#  Nikulin Vasily © 2021
from flask import render_template

from data import db_session
from data.teachers import Teacher
from site_app import site


@site.route('/teachers', methods=['GET'])
def teachers():
    db_sess = db_session.create_session()
    teachers_data = db_sess.query(Teacher.id, Teacher.surname, Teacher.name, Teacher.patronymic,
                                  Teacher.subject, Teacher.about).all()

    return render_template("site/teachers.html",
                           teachers=teachers_data,
                           title='Руководство и педагогический состав')
