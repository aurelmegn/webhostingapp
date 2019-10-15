from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ChangeInfoForm(FlaskForm):
    name = StringField("Name".capitalize(), validators=[DataRequired()])
    country = StringField("Country".capitalize(), validators=[DataRequired()])
    town = StringField("Town".capitalize(), validators=[DataRequired()])
    address = StringField("Address".capitalize(), validators=[DataRequired()])
    number = StringField("Number".capitalize(), validators=[DataRequired()])
