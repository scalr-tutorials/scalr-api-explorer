#coding:utf-8
import os
import StringIO

import lxml.etree as etree
from flask import Flask, make_response, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from pygments import highlight
from pygments import lexers
from pygments import formatters

import forms, client


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')

formatter = formatters.HtmlFormatter(linenos=True)

STORED_KEYS = ["api_key", "api_secret", "environment_id"]

@app.route('/', methods=["GET", "POST"])
def home():
    """Render website's home page."""
    kwargs = dict(((k, session.get(k)) for k in STORED_KEYS))
    form = forms.FireEventForm(**kwargs)

    if form.validate_on_submit():
        for key in STORED_KEYS:
            session[key] = getattr(form, key).data
        code, xml_body = client.fire_custom_event(form.api_key.data, form.api_secret.data, form.server_id.data, form.event_name.data, form.environment_id.data)

        try:
             doc = etree.parse(StringIO.StringIO(xml_body))
             body = etree.tostring(doc, pretty_print=True)
        except etree.XMLSyntaxError:
            body = xml_body

        try:
            lexer = lexers.guess_lexer(body)
            body = highlight(body, lexer, formatter)
        except lexers.ClassNotFound:
            pass
        return render_template('home.html', form=form, code=code, body=body)
    return render_template('home.html', form=form)


@app.route('/code-style.css')
def get_styles():
    response = make_response(formatter.get_style_defs(".highlight"))
    response.headers["Content-Type"] = "text/css"
    return response


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
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
