import os

from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap

import forms, client


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

###
# Routing for your application.
###

@app.route('/', methods=["GET", "POST"])
def home():
    """Render website's home page."""
    form = forms.FireEventForm()
    if form.validate_on_submit():
        code, body = client.fire_custom_event(form.api_key.data, form.secret_key.data, form.server_id.data,
                                              form.event_name.data, form.environment_id.data)
        return render_template('home.html', form=form, code=code, body=body)
    return render_template('home.html', form=form)

###
# The functions below should be applicable to all Flask apps.
###

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
