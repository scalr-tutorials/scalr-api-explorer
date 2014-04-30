#coding:utf-8
import datetime
import base64
import hmac
import hashlib

from geventhttpclient import HTTPClient
from geventhttpclient.url import URL


API_URL = 'https://api.scalr.net/'
API_VERSION = '2.3.0'
API_AUTH_VERSION = '3'

def fire_custom_event(api_key, api_secret, api_method, environment_id, api_call_data):
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    api_key = api_key.encode("utf-8")
    api_secret = api_secret.encode("utf-8")

    params = {
        "Action": api_method,
        "EnvID": environment_id,
        "Version": API_VERSION,
        "AuthVersion": API_AUTH_VERSION,
        "Timestamp": timestamp,
        "KeyID": api_key,
        "Signature":  base64.b64encode(hmac.new(api_secret, ":".join([api_method, api_key, timestamp]), hashlib.sha256).digest()),
    }
    params.update(api_call_data)

    url = URL(API_URL)

    for k, v in params.items():
      url[k] = v

    http = HTTPClient.from_url(url)
    response = http.get("/?" + url.query_string)

    code = response.status_code
    body = response.read()

    http.close()

    return url, code, body
