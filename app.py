import os

from flask import Flask, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap

import forms, client


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

STORED_KEYS = ["api_key", "api_secret", "environment_id"]

@app.route('/', methods=["GET", "POST"])
def home():
    """Render website's home page."""
    kwargs = dict(((k, session.get(k)) for k in STORED_KEYS))
    print "KWARGS", kwargs
    form = forms.FireEventForm(**kwargs)

    print "SESSION", session

    if form.validate_on_submit():
        for key in STORED_KEYS:
            session[key] = getattr(form, key).data
        code, body = client.fire_custom_event(form.api_key.data, form.api_secret.data, form.server_id.data, form.event_name.data, form.environment_id.data)
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
