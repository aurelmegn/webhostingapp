from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

from src.forms.all_from_enum import all_from_enum
from src.models.Application import AppType


class ApplicationForm(FlaskForm):
    name = StringField("name".capitalize(), validators=[DataRequired()])
    description = TextAreaField("description".capitalize(), validators=[DataRequired()])
    type = SelectField(
        "type".capitalize(), choices=all_from_enum(AppType), validators=[DataRequired()]
    )


class ApplicationEditForm(FlaskForm):
    description = TextAreaField("description".capitalize(), validators=[])
    domain_name = StringField("domain name".capitalize(), validators=[])
    entrypoint = StringField("entrypoint".capitalize(), validators=[DataRequired()])
    callable = StringField("callable".capitalize(), validators=[DataRequired()])
