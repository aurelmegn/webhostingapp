from pyexpat import ExpatError

from flask import render_template, request, abort
from flask_login import login_required, current_user
from flask_security import roles_required
from xmlrpc.client import Fault

from src.models.Application import AppState
from src.models import Application
from src import app, supervisor
from src.utils.tail import tail


@app.route("/dashboard", methods=["get"])
@login_required
@roles_required("user")
def dashboard():
    selected_app = request.args.get("appname") or None

    # order the applications of the user // todo
    # current_user.applications

    from src.forms.ApplicationForm import ApplicationForm

    create_app_form = ApplicationForm()

    ftp_host = app.config.get("FTP_HOST")
    ftp_port = app.config.get("FTP_PORT")

    if selected_app:

        application = Application.query.filter_by(
            user=current_user, name=selected_app
        ).first()

        if not application:
            abort(404)

        err_log = None
        out_log = None

        if application.state != AppState.never_started:
            try:
                app_supervisor_name = application.get_supervisor_name()

                err_log: [str] = supervisor.tailProcessStderrLog(
                    app_supervisor_name, True, 4000
                )
                out_log = tail(application.get_out_for_supervisor_log_path(), 1000)

                err_log = err_log[0]
                out_log = "".join(out_log) if type(out_log) == list else out_log

            except OSError as e:
                app.logger.error(e)
                # abort(500)
            except Fault as e:
                app.logger.error(e)
                abort(500)

        return render_template(
            "default/dashboard/select_app.jinja",
            user=current_user,
            caform=create_app_form,
            application=application,
            AppState=AppState,
            app_out_log=out_log,
            ftp_host=ftp_host,
            ftp_port=ftp_port,
        )

    return render_template(
        "default/dashboard_base.jinja",
        user=current_user,
        caform=create_app_form,
        ftp_host=ftp_host,
        ftp_port=ftp_port,
    )
