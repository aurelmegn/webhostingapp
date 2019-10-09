from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired

from src.forms.all_from_enum import all_from_enum
from src.models.Application import AppType


class ApplicationForm(FlaskForm):
    name = StringField("name".capitalize(), validators=[DataRequired()])
    description = TextAreaField("description".capitalize(), validators=[DataRequired()])
    type = SelectField("type".capitalize(), choices=all_from_enum(AppType), validators=[DataRequired()])


class ApplicationEditForm(FlaskForm):
    entrypoint = TextAreaField("entrypoint".capitalize(), validators=[DataRequired()])

    def __init__(self):

        super()
        self.__delitem__("name")
        self.__delitem__("type")
