from flask import Blueprint, make_response, redirect, render_template, request, url_for

from flask_login import current_user
from src import db
from src.forms.settings.AccountForms import ChangeInfoForm
from src.models import User

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.route("/")
def index():
    form = ChangeInfoForm()

    user = User.query.filter_by(id=current_user.id)

    if form.validate_on_submit():

        form.populate_obj(user)
        db.session.commit()

        return redirect(request.referrer)

    elif request.args.get("export_data"):
        # export data into a format
        return make_response()

    elif request.args.get("delete_account"):
        # delete the account and logout
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("logout"))

    return render_template("default/settings/index.jinja", user=current_user, form=form)


@settings_bp.route("/security")
def security():
    return render_template("default/settings/security.jinja", user=current_user)


@settings_bp.route("/notifications")
def notifications():
    return render_template("default/settings/notifications.jinja", user=current_user)


@settings_bp.route("/emails")
def emails():
    return render_template("default/settings/emails.jinja", user=current_user)


@settings_bp.route("/billing")
def billing():
    return render_template("default/settings/billing.jinja", user=current_user)
