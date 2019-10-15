from flask import Blueprint, render_template
from flask_login import current_user

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.route("/")
def index():
    return render_template("default/settings/index.jinja", user=current_user)


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
