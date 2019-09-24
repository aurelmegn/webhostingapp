from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import DataRequired


class ApplicationForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    description = TextAreaField("description", validators=[DataRequired()])
