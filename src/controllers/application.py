import subprocess
from flask import (
    request,
    abort,
    flash,
    redirect,
    url_for,
    jsonify,
    render_template,
    session,
)
from flask_login import login_required, current_user
from flask_security import roles_required
from string import Template
from xmlrpc.client import Fault

from src.models.Application import AppState, AppType
from src import app, supervisor
from src.models import Application
from src.models import User
from src.utils.find_or_create import find_or_create

from os.path import join, isdir, abspath
from shutil import rmtree


@app.route("/application/execute_cmd", methods=["post"])
@login_required
@roles_required("user")
def app_execute_cmd():
    selected_app = request.args.get("appname")
    command = request.form["command"]

    session.pop(f"last_cmd_{selected_app}", None)

    if not (command or selected_app):
        abort(404)

    application = Application.query.filter_by(
        user=current_user, name=selected_app
    ).first()

    if not application:
        abort(404)

    # check if the application is python type
    if application.type in [AppType.python37, AppType.python36, AppType.python35]:

        app_dir = application.get_app_ftp_dir()
        try:
            bin_path = join(app_dir, "venv", "bin")

            # if command.split()[0] == "pip":
            #     # remove the pip and replace it with python -m
            #     splited_cmd = command.split()
            #     splited_cmd = " ".join(splited_cmd[1:])
            #
            #     reformed_cmd = f"firejail --quiet --private {bin_path}/python -m pip {splited_cmd}".split()
            #
            # else:
            reformed_cmd = f"firejail --quiet --private {bin_path}/{command}".split()

            app.logger.debug(" ".join(reformed_cmd))

            output = subprocess.run(
                reformed_cmd,
                stdout=subprocess.PIPE,
                # stderr=subprocess.PIPE,
                check=True,
                timeout=10,  # exit after 10sec
            )

            # app.logger.debug(output.stderr.decode("utf-8"))
            output = output.stdout.decode("utf-8")

            session[f"last_cmd_{selected_app}"] = {"output": output, "cmd": command}

        except Exception as e:
            app.logger.error(e)
            flash(f"command {command} can not be executed")
        except OSError as e:
            app.logger.error(e)
            flash(f"command {command} can not be executed")

        # if the app is php type

    return redirect(request.referrer)


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

        action_executed = False

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

                if user_app.type in [
                    AppType.python37,
                    AppType.python36,
                    AppType.python35,
                ]:
                    app_dir = user_app.get_app_ftp_dir()

                    env_path = join(app_dir, "venv")
                    # remove the venv dir on the application ftp dir
                    if isdir(env_path):
                        rmtree(env_path)

                    import virtualenv

                    try:
                        virtualenv.create_environment(
                            env_path, clear=True, no_setuptools=True, no_wheel=True
                        )
                    except subprocess.CalledProcessError as e:
                        app.logger.error(e)
                        abort(500)

                    # write supervisor config into it destination
                    write_supervisor_conf(application=user_app)

                    # write uwsgi config into it destination
                    write_uwsgi_conf(application=user_app)

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
        flash(f"Error during application {action} operation: {e.faultString}", "error")
        # abort(500, e)

    return redirect(request.referrer)


def write_uwsgi_conf(application: Application = None):
    # create the uwsgi config file
    uwsgi_template_path = app.config.get("UWSGI_TEMPLATE_PATH")
    uwsgi_template_path = abspath(uwsgi_template_path)

    config = create_uwsgi_conf(current_user, application, uwsgi_template_path)

    # move the config into the correct directory
    user_conf_dir = current_user.get_supervisor_conf_dir()

    # create the directory if it does not exist
    find_or_create(user_conf_dir)

    # create the file and fill it with the config file
    app_conf_path = application.get_uwsgi_conf_path()
    with open(app_conf_path, "w") as f:
        f.write(config)


def create_uwsgi_conf(user: User, application: Application, path: str):
    # read the content of the file
    with open(path) as f:
        content = f.read().strip()

    # initialize the template string to substitute the template
    t = Template(content)

    # the venv folder of the app
    venv_folder = join(application.get_app_ftp_dir(), "venv")
    # initialise the parameters based on the current user and the application

    parameters = {
        "supervisor_program_name": application.get_supervisor_name(),
        "entrypoint": application.entrypoint,
        "program_ftpdir": application.get_app_ftp_dir(),
        "out_log": application.get_out_log_path(),
        "sock_path": application.get_uwsgi_sock_path(),
        "venv": venv_folder
    }

    return t.safe_substitute(parameters)


def write_supervisor_conf(application: Application = None):
    # add the app config to supervisor config dir
    supervisor_template_path = app.config.get("SUPERVISOR_PROGRAM_TEMPLATE_PATH")
    supervisor_template_path = abspath(supervisor_template_path)

    config = create_supervisor_config(current_user, application, supervisor_template_path)

    # move the config into the correct directory
    user_conf_dir = current_user.get_supervisor_conf_dir()

    # create the directory if it does not exist
    find_or_create(user_conf_dir)

    # create the file and fill it with the config file
    app_conf_path = application.get_supervisor_conf_path()
    with open(app_conf_path, "w") as f:
        f.write(config)


def create_supervisor_config(application: Application, path: str) -> str:
    # read the content of the file
    with open(path) as f:
        content = f.read().strip()

    # initialize the template string to substitute the template
    t = Template(content)

    parameters = {
        "supervisor_program_name": application.get_supervisor_name(),
        "uwsgi_conf": application.get_uwsgi_conf_path(),
        "program_ftpdir": application.get_app_ftp_dir(),
        "out_log": application.get_out_log_path(),
        "err_log": application.get_err_log_path(),
    }

    return t.safe_substitute(parameters)
