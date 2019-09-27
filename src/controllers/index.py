from xmlrpc.client import Fault

from src import db, supervisor, app
from flask import (
    render_template,
    request,
    abort,
    jsonify,
    flash,
    redirect,
    url_for,
    make_response,
)
from flask_security import login_required, current_user, roles_required

from src.models.Application import Application

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

    # order the applications of the user
    current_user.applications
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


@app.route("/application/action")
@login_required
@roles_required("user")
def app_action():

    # get the app name from the request
    app_name = request.args.get("name")
    action = request.args.get("action")

    actions = ["start", "stop", "restart"]

    if not action:
        abort(400)

    if not (app_name or action.lower() not in actions):
        flash(f"An error occured", "dashboard_error")
        return redirect(url_for("dashboard"))

    # check if the user own an application of the same name
    user_app = Application.query.filter_by(name=app_name, user=current_user).first()

    if not user_app:
        abort(404)

    print(action)

    try:
        # proceed to the application action specified
        if action == "start":
            supervisor.startProcess(user_app.get_supervisor_name())
        elif action == "stop":
            supervisor.stop(user_app.get_supervisor_name())
        elif action == "restart":
            supervisor.restart(user_app.get_supervisor_name())

        flash(f"Application {app_name} {action}ed", "dashboard_info")

    except ConnectionRefusedError as e:
        app.logger.info(str(e) + "unable to connect to supervisor instance")
        abort(500)
        print(e)
    except Fault as e:
        app.logger.info(str(e))
        print(e)
        abort(500)

    return redirect(url_for("dashboard"))
