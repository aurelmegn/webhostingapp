from flask import request, abort, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask_security import roles_required
from string import Template
from xmlrpc.client import Fault

from src.models.Application import AppState
from src import app, supervisor, db
from src.models import Application
from src.models import User
from src.utils.find_or_create import find_or_create


@app.route("/application/state")
@login_required
@roles_required("user")
def app_info():
    """get a running app info"""
    # get the app name from the request
    app_name = request.args.get("name")

    if not app_name:
        flash(f"An error occurred", "error")
        return redirect(url_for("dashboard"))
    # check if the user own an application of the same name

    user_app = Application.query.filter_by(name=app_name, user=current_user).first()

    if not user_app:
        abort(404)

    # check is the app is enabled
    if not user_app.enabled:
        abort(400)

    try:
        process_info = supervisor.getProcessInfo(user_app.get_supervisor_name())

        # get the state of the app and update it accordingly into the database 
        return jsonify(process_info)

    except ConnectionRefusedError as e:
        app.logger.info(str(e) + "unable to connect to supervisor instance")
        abort(500)
        print(e)
    except Fault as e:
        app.logger.info(str(e))
        abort(500)


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
        flash(f"An error occurred", "error")
        return redirect(url_for("dashboard"))
    # check if the user own an application of the same name

    user_app = Application.query.filter_by(name=app_name, user=current_user).first()

    if not user_app:
        abort(404)

    # check is the app is enabled
    if not user_app.enabled:
        abort(400)

    print(action)

    try:
        # proceed to the application action specified
        if action == "start":
            # todo
            """
                if the app has never been started 
                create the config for supervisor
                move it on the right dir
                add it as an supervisor app
                change the state of the application
                start it

            """
            if user_app.state is AppState.never_started:
                path = app.config.get("SUPERVISOR_PROGRAM_TEMPLATE_PATH")
                config = create_supervisor_config(current_user, user_app, path)
                # print(config)
                # move the config into the correct directory

                user_conf_dir = current_user.get_supervisor_conf_dir()

                # create the directory if it does not exist
                find_or_create(user_conf_dir)

                # create the file and fill it with the config file
                app_conf_path = user_app.get_supervisor_conf_path()
                with open(app_conf_path, 'w') as f:
                    f.write(config)

                supervisor.reloadConfig()
                supervisor.addProcessGroup(user_app.get_supervisor_name())

            else:  # if the app have been started
                supervisor.startProcess(user_app.get_supervisor_name())

            user_app.state = AppState.starting

        elif action == "stop":
            supervisor.stopProcess(user_app.get_supervisor_name())
            user_app.state = AppState.stopping
        elif action == "restart":
            supervisor.reloadConfig()
            supervisor.stopProcess(user_app.get_supervisor_name())
            supervisor.startProcess(user_app.get_supervisor_name())

            user_app.state = AppState.starting

        db.session.add(user_app)
        db.session.commit()

        action = "stopped" if action == "stop" else action + "ed"
        flash(f"Application {app_name} {action}", "dashboard:info")

    except ConnectionRefusedError as e:
        app.logger.critical(str(e) + "unable to connect to supervisor instance")
        abort(500, e)
        print(e)
    except Fault as e:
        app.logger.critical(e)
        # print(e)
        flash(f"Error durring application {action} operation: {e.faultString}", "error")
        # abort(500, e)

    return redirect(url_for("dashboard"))


def create_supervisor_config(user: User, application: Application, path: str) -> str:
    # read the content of the file
    with open(path) as f:
        content = f.read().strip()

    # initialize the template string to substitute the template
    t = Template(content)

    # initialise the parameters based on the current user and the application
    parameters = {
        "supervisor_program_name": application.get_supervisor_name(),
        "entrypoint": application.entry_point,
        "program_ftpdir": application.get_app_ftp_dir(),
        "username": user.username,
        "program_name": application.name,
    }

    return t.safe_substitute(parameters)
