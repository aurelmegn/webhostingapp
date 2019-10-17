import subprocess
from os import mknod
from os.path import abspath, isdir, join
from string import Template
from xmlrpc.client import Fault

from flask import abort, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_security import roles_required
from sqlalchemy import asc, desc

from src import app, db, supervisor
from src.forms.ApplicationForm import ApplicationForm
from src.models import AppActionHistory, Application
from src.models.Application import AppState, AppType
from src.utils.find_or_create import find_or_create


@app.route("/application/install_requirements/<string:appname>", methods=["post"])
@login_required
@roles_required("user")
def app_install_requirements(appname):
    req_file_name = request.form["req_file_name"]

    if not req_file_name:
        abort(404)

    application = Application.query.filter_by(user=current_user, name=appname).first()

    if not application:
        abort(404)

    # check if the application is python type
    if application.type in [AppType.python37, AppType.python36, AppType.python35]:

        app_dir = application.get_app_ftp_dir()
        try:
            bin_path = join("venv", "bin")
            firejail_profile = abspath(app.config.get("FIREJAIL_PROFILE"))

            cmd = f"firejail --quiet --profile={firejail_profile} {bin_path}/python -m pip install -r {req_file_name}".split()

            app.logger.debug(" ".join(cmd))

            output = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                # stderr=subprocess.PIPE,
                check=True,
                timeout=10,  # exit after 10sec
                cwd=app_dir,
            )

            # app.logger.debug(output.stderr.decode("utf-8"))
            output = output.stdout.decode("utf-8")

            flash(
                f"Requirements installed successfully for {application.name}", "success"
            )

        except (Exception, OSError) as e:
            app.logger.error(e)
            flash(
                f"An error occurred. Can not install the requirements. Is the file name well written ?"
            )

        # if the app is php type

    return redirect(request.referrer)


@app.route("/application/state/<string:appname>")
@login_required
@roles_required("user")
def app_info(appname):
    """get a running app info"""

    # check if the user own an application of the same name
    user_app = Application.query.filter_by(name=appname, user=current_user).first()

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


@app.route("/application/action/<string:appname>")
@login_required
@roles_required("user")
def app_action(appname):
    # get the app name from the request
    action = request.args.get("action")

    actions = ["start", "stop", "restart"]

    if not action:
        abort(400)

    if not (appname or action.lower() not in actions):
        flash(f"An error occurred", "error")
        return redirect(url_for("dashboard"))
    # check if the user own an application of the same name

    application = Application.query.filter_by(name=appname, user=current_user).first()

    if not application:
        abort(404)

    # check is the app is enabled
    if not application.enabled:
        abort(404)

    app_action_history = AppActionHistory(old_state=application.state, action=action)

    try:

        action_executed = False

        # proceed to the application action specified
        if action == "start" and application.can_start():
            # todo
            """
                if the app has never been started 
                create the config for supervisor
                move it on the right dir
                add it as an supervisor app
                change the state of the application
                start it

            """
            if application.state is AppState.never_started:

                app_generate_config_and_start_subprogram(application)
                supervisor.addProcessGroup(application.get_supervisor_name())

                generate_nginx_conf(application)
                send_sig_hup_nginx()

            elif application.state in [
                AppState.stopped,
                AppState.backoff,
                AppState.fatal,
                AppState.unknown,
            ]:  # if the app have been started
                app_generate_config_and_start_subprogram(application)
                supervisor.startProcess(application.get_supervisor_name())

            else:  # if the app have been started
                supervisor.startProcess(application.get_supervisor_name())

            action_executed = True
        elif action == "stop" and application.can_stop():
            supervisor.stopProcess(application.get_supervisor_name())
            # application.state = AppState.stopping

            action_executed = True

        elif action == "restart" and application.can_restart():
            supervisor.stopProcess(application.get_supervisor_name())
            app_generate_config_and_start_subprogram(application)
            supervisor.reloadConfig()
            supervisor.startProcess(application.get_supervisor_name())

            # application.state = AppState.starting
            action_executed = True

        if action_executed:
            application.have_started_once = True
            action = "stopped" if action == "stop" else action + "ed"
            flash(f"Application {appname} {action}", "success")

    except ConnectionRefusedError as e:
        app.logger.critical(str(e) + "unable to connect to supervisor instance")
        abort(500, e)
        # print(e)
    except Fault as e:
        app.logger.critical(e)
        # print(e)
        flash(f"Error during application {action} operation: {e.faultString}", "error")
        # abort(500, e)

    # save the action in the history of action for the current application
    app_action_history.new_state = application.state
    application.action_histories.append(app_action_history)

    db.session.commit()

    return redirect(request.referrer)


@app.route("/application/add", methods=["post", "get"])
@login_required
@roles_required("user")
def app_add():
    application_form = ApplicationForm()

    applications = (
        Application.query.with_parent(current_user)
        .order_by(desc("enabled"), asc("name"))
        .all()
    )

    if application_form.validate_on_submit():
        # print(application_form.object_data)

        # if request.headers
        application = Application()
        application_form.populate_obj(application)
        application.type = AppType(application.type)

        # search for the same app name in the database

        count = application.query.filter_by(
            user=current_user, name=application.name
        ).count()

        if count != 0:
            flash("You already have an application of the same name", "error")

            return render_template(
                "default/dashboard/app_create.jinja",
                addform=application_form,
                user=current_user,
            )

        current_user.applications.append(application)
        db.session.commit()

        return redirect(url_for("dashboard", appname=application.name))

    return render_template(
        "default/dashboard/app_create.jinja",
        addform=application_form,
        user=current_user,
        applications=applications,
    )


def write_uwsgi_conf(application: Application = None):
    # create the uwsgi config file
    uwsgi_template_path = app.config.get("UWSGI_TEMPLATE_PATH")
    uwsgi_template_path = abspath(uwsgi_template_path)

    config = create_uwsgi_conf(application, uwsgi_template_path)

    # move the config into the correct directory
    user_conf_dir = current_user.get_supervisor_conf_dir()

    # create the directory if it does not exist
    find_or_create(user_conf_dir)

    # create the file and fill it with the config file
    app_conf_path = application.get_abs_uwsgi_conf_path()
    with open(app_conf_path, "w") as f:
        f.write(config)


def create_uwsgi_conf(application: Application, path: str):
    # read the content of the file
    with open(path) as f:
        content = f.read().strip()

    # initialize the template string to substitute the template
    t = Template(content)

    # the venv folder of the app
    # venv_folder = join(application.get_app_ftp_dir(), "venv")
    # initialise the parameters based on the current user and the application

    parameters = {
        "supervisor_program_name": application.get_supervisor_name(),
        "entrypoint": application.entrypoint,
        "program_ftpdir": application.get_app_ftp_dir(),
        "out_log": join(
            app.config.get("ABS_PATH_HOME_UWSGI"), application.get_out_log_path()
        ),
        "port": application.port,
        "venv": join(
            app.config.get("ABS_PATH_HOME_UWSGI"), "venv"
        ),  # get the absolute path on the sandbox
    }

    return t.safe_substitute(parameters)


def write_supervisor_conf(application: Application = None):
    # add the app config to supervisor config dir
    supervisor_template_path = app.config.get("SUPERVISOR_PROGRAM_TEMPLATE_PATH")
    supervisor_template_path = abspath(supervisor_template_path)

    config = create_supervisor_config(application, supervisor_template_path)

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
    print(application.get_out_log_path())
    parameters = {
        "supervisor_program_name": application.get_supervisor_name(),
        "uwsgi_conf": application.get_uwsgi_conf_path(),
        "program_ftpdir": application.get_app_ftp_dir(),
        # "out_log": application.get_out_log_path(),
        "out_for_supervisor_log": application.get_out_for_supervisor_log_path(),
        "err_log": application.get_err_log_path(),
        "profile": abspath(app.config.get("FIREJAIL_PROFILE")),
    }

    return t.safe_substitute(parameters)


def app_generate_config_and_start_subprogram(application):
    # create virtualenv if the app is python app

    if application.type in [AppType.python37, AppType.python36, AppType.python35]:
        app_dir = application.get_app_ftp_dir()

        env_path = join(app_dir, "venv")

        # remove the venv dir on the application ftp dir
        if not isdir(env_path):

            import virtualenv

            try:
                virtualenv.create_environment(
                    env_path, clear=True, no_setuptools=True, no_wheel=True
                )
            except subprocess.CalledProcessError as e:
                app.logger.error(e)
                abort(500)

        # write supervisor config into it destination
        write_supervisor_conf(application=application)

        # write uwsgi config into it destination
        write_uwsgi_conf(application=application)

    supervisor.reloadConfig()


def generate_nginx_conf(application: Application):
    template_conf_path = app.config.get("NGINX_CONF_TEMPLATE_PATH")

    # read the content of the file
    with open(template_conf_path) as f:
        content = f.read().strip()

    # initialize the template string to substitute the template
    t = Template(content)

    parameters = {
        "supervisor_program_name": application.get_supervisor_name(),
        "port": application.port,
        "domain_name": application.domain_name,
    }

    config = t.safe_substitute(parameters)
    app_conf_path = application.get_abs_nginx_conf_path()
    with open(app_conf_path, "w") as f:
        f.write(config)


def send_sig_hup_nginx():
    file_path = app.config.get("NGINX_HUP_CHECK_FILE")
    mknod(file_path)
