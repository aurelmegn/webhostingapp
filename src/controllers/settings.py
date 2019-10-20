from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_security.utils import hash_password, verify_password

from src import db
from src.forms.ApplicationForm import ApplicationEditForm
from src.forms.settings.AccountForms import (
    ChangeInfoForm,
    ChangePasswordForm,
    EmailForm,
    EmailPreferenceForm,
    PrimaryEmailSelectForm,
)
from src.models import User

settings_bp = Blueprint("settings", __name__, url_prefix="/settings")


@settings_bp.route("/security", methods=["post", "get"])
@login_required
def security():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        current_password = form.current.data
        new_password = form.new.data
        confirmed_password = form.confirm.data

        if new_password != confirmed_password:
            flash("Confirmation password provided doesn't match", "error")
            return redirect(request.referrer)

        if not verify_password(current_password, current_user.password):
            flash("Password provided does not match", "error")
            return redirect(request.referrer)

        current_user.password = hash_password(new_password)
        db.session.commit()

        flash("Password changed successfully", "success")

    return render_template(
        "default/settings/security.jinja", user=current_user, change_password_form=form
    )


@settings_bp.route("/", methods=["post", "get"])
@login_required
def index():
    form = ChangeInfoForm()
    # form=ApplicationEditForm()

    user = User.query.filter_by(id=current_user.id).first()

    if form.validate_on_submit():

        form.populate_obj(user)
        db.session.commit()

        flash("Information updated successfully", "success")
        return redirect(request.referrer)

    elif request.args.get("export_data"):
        # export data into a format
        return make_response()

    elif request.args.get("delete_account"):
        # delete the account and logout
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("logout"))

    # pre fill the form fields
    form.name.data = user.name
    form.country.data = user.country
    form.city.data = user.city
    form.address.data = user.address
    form.number.data = user.number

    return render_template(
        "default/settings/index.jinja", user=current_user, change_info_form=form
    )


@settings_bp.route("/notifications")
@login_required
def notifications():
    return render_template("default/settings/notifications.jinja", user=current_user)


@settings_bp.route("/emails")
@login_required
def emails():
    email_form = EmailForm()

    if email_form.validate_on_submit():
        pass

    # form to select primary email address
    primary_email_form = PrimaryEmailSelectForm()
    if primary_email_form.validate_on_submit():
        # i should change the current email of the user and set it to the new primary one
        pass

    primary_email_form.elements.choices = [
        (x.label, x.label) for x in current_user.emails
    ]

    # form to select backup email address
    backup_email_form = PrimaryEmailSelectForm()
    if backup_email_form.validate_on_submit():
        pass

    backup_email_form.elements.choices = [
        (x.label, x.label) for x in current_user.emails
    ]

    email_preference_form = EmailPreferenceForm()
    if email_preference_form.validate_on_submit():
        pass

    return render_template(
        "default/settings/emails.jinja",
        user=current_user,
        email_form=email_form,
        primary_email_form=primary_email_form,
        backup_email_form=backup_email_form,
        email_preference_form=email_preference_form,
    )


@settings_bp.route("/billing")
@login_required
def billing():
    return render_template("default/settings/billing.jinja", user=current_user)
