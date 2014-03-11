from flask_wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired

class FireEventForm(Form):
    api_key = TextField('API Key', validators=[DataRequired()])
    secret_key = TextField('Secret Key', validators=[DataRequired()])
    server_id = TextField('Server ID', validators=[DataRequired()])
    event_name = TextField('Event Name', validators=[DataRequired()])
    environment_id = TextField('Environment ID (Optional)')

