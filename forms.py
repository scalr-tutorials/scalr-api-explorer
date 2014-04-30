#coding:utf-8
from flask_wtf import Form
from wtforms import TextField, SelectField, HiddenField
from wtforms.validators import DataRequired

import api


method_choices = zip(api.API_STRUCTURE.keys(), api.API_STRUCTURE.keys())


class APIForm(Form):
    api_key = TextField('API Key', validators=[DataRequired()])
    api_secret = TextField('Secret Key', validators=[DataRequired()])
    environment_id = TextField('Environment ID (Optional)')
    method = SelectField("API Method", choices=method_choices, validators=[DataRequired()])
    no_call = HiddenField("No API Call")
