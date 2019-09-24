from src import app, db
from flask import render_template, request
from flask_security import login_required, current_user, roles_required

from src.models.User import User

#
@app.route("/")
@login_required
@roles_required("user")
def index():
    # return render_template("default/index.jinja")
    return "Hello world"


@app.route("/dashboard")
@login_required
@roles_required("user")
def dashboard():

    apps = current_user.applications

    # print(apps)

    from src.forms.ApplicationForm import ApplicationForm

    create_app_form = ApplicationForm()
    return render_template(
        "default/dashboard.jinja", user=current_user, caform=create_app_form
    )


#
# @app.route("/add_app")
# @login_required
# @roles_required('user')
# def add_app():
#
#     apps = current_user.applications
#
#     print(apps)
#
#     return render_template("default/dashboard.jinja", user=current_user)
