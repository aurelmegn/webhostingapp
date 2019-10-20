from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, RadioField
from wtforms.validators import DataRequired


class ChangeInfoForm(FlaskForm):
    name = StringField("Name".capitalize(), validators=[DataRequired()])
    country = StringField("Country".capitalize(), validators=[DataRequired()])
    city = StringField("City".capitalize(), validators=[DataRequired()])
    address = StringField("Address".capitalize(), validators=[DataRequired()])
    number = StringField("Number".capitalize(), validators=[DataRequired()])


class ChangePasswordForm(FlaskForm):
    current = PasswordField(
        "Current password".capitalize(), validators=[DataRequired()]
    )
    new = PasswordField("New password".capitalize(), validators=[DataRequired()])
    confirm = PasswordField(
        "Confirm password".capitalize(), validators=[DataRequired()]
    )


class EmailForm(FlaskForm):
    label = StringField("Label".capitalize(), validators=[])


class PrimaryEmailSelectForm(FlaskForm):
    elements = SelectField("Label".capitalize(), validators=[DataRequired()])


class EmailPreferenceForm(FlaskForm):
    elements = RadioField(
        "Email preferences",
        choices=[
            ("all", "Receive all emails, except those I unsubscribe from"),
            (
                "account_related",
                "Only receive account related emails, and those I subscribe to.",
            ),
        ],
    )
