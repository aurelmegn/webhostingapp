from flask import render_template, request, abort, redirect, url_for
from flask_login import login_required, current_user
from flask_security import roles_required
from sqlalchemy import asc, desc
from xmlrpc.client import Fault

from src.models.AppActionHistory import AppActionHistory
from src.forms.ApplicationForm import ApplicationEditForm, ApplicationForm
from src.utils.HelperClass import AppState
from src.models import Application
from src import app, supervisor, db
from src.utils.tail import tail


@app.route("/dashboard", methods=["get"])
@login_required
@roles_required("user")
def dashboard():
    appname = request.args.get("appname") or None

    # order the applications of the user // todo
    # current_user.applications

    create_app_form = ApplicationForm()

    ftp_host = app.config.get("FTP_HOST")
    ftp_port = app.config.get("FTP_PORT")

    applications = (
        Application.query.with_parent(current_user)
        .order_by(desc("enabled"), asc("name"))
        .all()
    )

    if appname:

        application = Application.query.filter_by(
            user=current_user, name=appname
        ).first()

        actions_histories = (
            AppActionHistory.query.with_parent(application)
            .order_by(desc("at"))
            .limit(20)
            .all()
        )

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
            applications=applications,
            caform=create_app_form,
            application=application,
            actions_histories=actions_histories,
            AppState=AppState,
            app_out_log=out_log,
            ftp_host=ftp_host,
            ftp_port=ftp_port,
        )

    return render_template(
        "default/dashboard_base.jinja",
        user=current_user,
        applications=applications,
        caform=create_app_form,
        ftp_host=ftp_host,
        ftp_port=ftp_port,
    )


@app.route("/application/edit/<string:appname>", methods=["get", "post"])
def app_edit(appname):
    ftp_host = app.config.get("FTP_HOST")
    ftp_port = app.config.get("FTP_PORT")

    application = Application.query.filter_by(user=current_user, name=appname).first()

    if not application:
        abort(404)

    caform = ApplicationForm()
    edit_app_form = ApplicationEditForm()

    if edit_app_form.validate_on_submit():
        edit_app_form.populate_obj(application)
        db.session.commit()

        return redirect(url_for("dashboard", appname=application.name))

    edit_app_form.description.data = application.description
    edit_app_form.callable.data = application.callable
    edit_app_form.domain_name.data = application.domain_name
    edit_app_form.entrypoint.data = application.entrypoint

    return render_template(
        "default/dashboard/edit_app.jinja",
        user=current_user,
        edform=edit_app_form,
        caform=caform,
        application=application,
        AppState=AppState,
        ftp_host=ftp_host,
        ftp_port=ftp_port,
    )
