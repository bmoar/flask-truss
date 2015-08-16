from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class _Form(Form):
    field = StringField(validators=[DataRequired()])
