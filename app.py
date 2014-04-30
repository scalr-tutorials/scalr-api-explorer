#coding:utf-8
import os
import StringIO

import lxml.etree as etree
from flask import Flask, make_response, render_template, request, redirect, url_for, session
from flask_bootstrap import Bootstrap
from wtforms import TextField, SelectField
from wtforms.validators import DataRequired

from pygments import highlight
from pygments import lexers
from pygments import formatters

import forms, client, api


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app

app = create_app()
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'this_should_be_configured')  #TODO

formatter = formatters.HtmlFormatter(linenos=True)

DEFAULT_API_CALL = "ServerLaunch"
STORED_KEYS = ["api_key", "api_secret", "method", "environment_id"]

@app.route('/', methods=["GET", "POST"])
def home():
    """Render website's home page."""
    kwargs = dict(((k, session.get(k)) for k in STORED_KEYS))
    api_only_form = forms.APIForm(**kwargs)

    if api_only_form.validate_on_submit():
        # Save data
        for key in STORED_KEYS:
            session[key] = getattr(api_only_form, key).data

    skip_api_call = api_only_form.no_call.data == "1"

    # Form for the actual API Call
    class CompleteForm(forms.APIForm):
        pass

    if api_only_form.method.validate(api_only_form):
        api_call = api_only_form.method.data
    else:
        api_call = DEFAULT_API_CALL

    for field, options in api.API_STRUCTURE.get(api_call, {}).items():
        validators = []
        if not options["optional"]:
            validators.append(DataRequired())
        setattr(CompleteForm, field, TextField(field, validators=validators))
    form = CompleteForm(**kwargs)

    if not skip_api_call and form.validate_on_submit():
        # We need to extract the data from the form
        non_data_fields = set((field.name for field in api_only_form))
        api_call_data = dict((field.name, field.data) for field in form if field.name not in non_data_fields)

        req, code, xml_body = client.fire_custom_event(form.api_key.data, form.api_secret.data, form.method.data, form.environment_id.data, api_call_data)

        # Formatting for the XML response
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

        # Formatting for the HTTP request
        key_id_token, signature_token = "this-is-key", "this-is-sign"  # Hack.
        req["KeyID"] = key_id_token
        req["Signature"] = signature_token
        req = req.query_string.replace("&", "\n&")\
                 .replace(key_id_token, "<Your Scalr API Key ID>")\
                 .replace(signature_token, "<URLEncode(Base64Encode(Signature))>")

        return render_template('home.html', form=form, req=req, code=code, body=body)

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
    response.headers['Cache-Control'] = 'no-cache'
    return response

@app.errorhandler(404)
def page_not_found(error):
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
