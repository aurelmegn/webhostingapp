import subprocess
from flask import request, abort, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from flask_security import roles_required
from string import Template
from xmlrpc.client import Fault

from src.models.Application import AppState, AppType
from src import app, supervisor, db
from src.models import Application
from src.models import User
from src.utils.find_or_create import find_or_create

import venv
from os.path import join, isdir
from shutil import rmtree

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
        # print(e)
    except Fault as e:
        app.logger.info(str(e))
        abort(500)


@app.route("/application/action")
@login_required
@roles_required("user")
def app_action():
    # get the app name from the request
    app_name = request.args.get("appname")
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

    try:

        action_executed=False

        # proceed to the application action specified
        if action == "start" and user_app.can_start():
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

                # create virtualenv if the app is python app

                if user_app.type in [AppType.python37, AppType.python36, AppType.python35]:
                    app_dir = user_app.get_app_ftp_dir()


                    env_path = join(app_dir, "venv")
                    # remove the venv dir on the application ftp dir
                    if isdir(env_path):
                        rmtree(env_path)

                    try:
                        venv.create(env_path, system_site_packages=False, with_pip=True)
                    except subprocess.CalledProcessError as e:
                        app.logger.error(e)
                        abort(500)

                    # subprocess.call()
                # add the app config to supervisor config dir
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

            action_executed = True
        elif action == "stop" and user_app.can_stop():
            supervisor.stopProcess(user_app.get_supervisor_name())
            # user_app.state = AppState.stopping

            action_executed = True

        elif action == "restart" and user_app.can_restart():
            supervisor.reloadConfig()
            supervisor.stopProcess(user_app.get_supervisor_name())
            supervisor.startProcess(user_app.get_supervisor_name())

            # user_app.state = AppState.starting
            action_executed = True

        if action_executed:
            action = "stopped" if action == "stop" else action + "ed"
            flash(f"Application {app_name} {action}", "success")

    except ConnectionRefusedError as e:
        app.logger.critical(str(e) + "unable to connect to supervisor instance")
        abort(500, e)
        # print(e)
    except Fault as e:
        app.logger.critical(e)
        # print(e)
        flash(f"Error durring application {action} operation: {e.faultString}", "error")
        # abort(500, e)

    return redirect(request.referrer)


def create_supervisor_config(user: User, application: Application, path: str) -> str:
    # read the content of the file
    with open(path) as f:
        content = f.read().strip()

    # initialize the template string to substitute the template
    t = Template(content)

    # the venv folder of the app
    venv_bin_folder = join(application.get_app_ftp_dir(), "venv/bin/")
    # initialise the parameters based on the current user and the application
    parameters = {
        "supervisor_program_name": application.get_supervisor_name(),
        "entrypoint": application.entrypoint,
        "program_ftpdir": application.get_app_ftp_dir(),
        "username": user.username,
        "program_name": application.name,
        "pip": join(venv_bin_folder, 'pip'),
        "python": join(venv_bin_folder, 'python'),
    }

    return t.safe_substitute(parameters)
