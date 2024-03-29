from flask import abort, jsonify, make_response, request
from flask_security import current_user, login_required, roles_required

from src import app, db
from src.forms.ApplicationForm import ApplicationForm
from src.models.Application import Application, AppType


@app.route("/api/app", methods=["post"])
@login_required
@roles_required("user")
def api_app_post():
    application_form = ApplicationForm()

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
            err = {"message": "You already have an application of the same name"}
            return make_response(jsonify(err), 400)

        current_user.applications.append(application)
        db.session.commit()

        return jsonify(application.__json__())

    else:
        app.logger.error(application_form.errors)
        abort(401)


@app.route("/api/app", methods=["get"])
@login_required
@roles_required("user")
def api_app_get():
    args_dic = dict(request.args)
    # search for the same app name in the database

    apps = Application.query.filter_by(**args_dic).all()

    if len(apps) == 0:
        return make_response("", 404)

    return jsonify([app.__json__() for app in apps])


# todo update or delete this part of the code
@app.route("/api/app", methods=["put"])
@login_required
@roles_required("user")
def api_app_reload():

    # check if the requets is for an reload
    is_reload = request.args.get("reload")
    if is_reload == 1:
        from xmlrpc.client import ServerProxy

        server = ServerProxy("http://localhost:9001/RPC2")

        # get the app name from the request

        app_name = request.json["name"]

        if not app_name:
            abort(jsonify(err="Missing the application name"), 400)

        # check if the user own an application of the same name
        user_app = Application.query.filter_by(name=app_name, user=current_user)

        if not user_app:
            abort(jsonify(err="You don't own such application"), 400)

        # proceed to the application reload

        server.supervisor.restart(app.get_supervisor_name())
        # reload the app from the bash
        pass

    # return jsonify(application)
    return ""
