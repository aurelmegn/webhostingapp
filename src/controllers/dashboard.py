from flask import render_template
from flask_login import login_required, current_user
from flask_security import roles_required

from src import app


@app.route("/dashboard")
@login_required
@roles_required("user")
def dashboard():
    apps = current_user.applications

    # print(apps)

    # order the applications of the user // todo
    current_user.applications
    from src.forms.ApplicationForm import ApplicationForm

    create_app_form = ApplicationForm()
    return render_template(
        "default/dashboard.jinja", user=current_user, caform=create_app_form
    )
