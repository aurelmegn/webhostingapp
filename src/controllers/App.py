import json
from flask import jsonify, request, Response, make_response
from flask_security import current_user, login_required, roles_required

from src import app, db
from src.models.User import User
from src.models.Application import Application


@app.route("/api/app", methods=["post"])
@login_required
@roles_required("user")
def app_post():
    # if request.headers
    application = Application()
    # print(request.json)
    application.name = request.json["name"]

    # search for the same app name in the database

    count = application.query.filter_by(user=current_user, name=application.name).count()

    if count != 0:
        err = {"message": "You already have an application of the same name"}
        return make_response(jsonify(err), 400)

    current_user.applications.append(application)
    db.session.commit()

    return jsonify(application.__json__())


@app.route("/api/app", methods=["get"])
@login_required
@roles_required("user")
def app_get():
    args_dic = dict(request.args)
    # search for the same app name in the database

    apps = Application.query.filter_by(**args_dic).all()

    if len(apps) == 0:
        return make_response("", 404)

    return jsonify([app.__json__() for app in apps])


@app.route("/api/app", methods=["put"])
@login_required
@roles_required("user")
def app_reload():
    is_reload = request.json["reload"]

    if is_reload:
        # reload the app from the bash
        pass

    # return jsonify(application)
    return ""
