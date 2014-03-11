from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

class FireEventForm(Form):
    api_key = TextField('api_key', validators=[DataRequired()])
    secret_key = TextField('secret_key', validators=[DataRequired()])
    server_id = TextField('server_id', validators=[DataRequired()])
    event_name = TextField('event_name', validators=[DataRequired()])
    environment_id = TextField('environment_id')

