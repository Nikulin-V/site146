#  Nikulin Vasily, Zhikharev Victor © 2021
from flask import render_template

from site_app import site


@site.route('/school_plan')
def school_plan():
    return render_template("site/school_plan.html",
            title="План школы")
