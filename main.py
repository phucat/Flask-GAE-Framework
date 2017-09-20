import logging

from app.exceptions import CustomException
from app.modules.dashboard.dashboard_api import dashboard
from app.modules.gcloud_samples.gcloud_api import gcloud
from app.modules.guestbook.guestbook_api import guestbook
from app.modules.helloworld.hello_word_api import hello_world
from app.modules.login.api import login
from core.auth import validate_authentication_header

from core.config import _is_app_spot
from core.config import _is_testbed
from flask import Flask, jsonify
from flask import request

from core.cross_domain import crossdomain

app = Flask(__name__)
app.secret_key = 'super secret key'
app.config.update(DEBUG=(not _is_app_spot() or _is_testbed()))

app.register_blueprint(login)
app.register_blueprint(hello_world)
app.register_blueprint(guestbook)
app.register_blueprint(gcloud)
app.register_blueprint(dashboard)



@app.before_request
def auth_user():
    """
    executed before entering blueprint endpoints
    """

    logging.info(request.headers)
    validate_authentication_header(request)


@app.after_request
def add_header(response):
    """
    allow request from any source
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, nothing at this URL.', 404


@app.errorhandler(500)
def server_error(e):
    """Return a custom 500 error."""
    return 'Error while serving request', 500


@app.errorhandler(CustomException)
def handle_invalid_usage(error):
    """
    used to return a json formatted version of the error upon request
    :param error:
    :return:
    """
    logging.warn(error.message)
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.after_request
@crossdomain(origin="*", headers='content-type, google-id-token')
def after_request(response):
    return response