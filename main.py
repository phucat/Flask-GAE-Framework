import logging

from app.exceptions import CustomException
from app.modules.dashboard.dashboard_api import dashboard
from app.modules.gcloud_samples.gcloud_api import gcloud
from app.modules.guestbook.guestbook_api import guestbook
from app.modules.helloworld.hello_word_api import hello_world
from core.auth import validate
from core.config import _is_app_spot, Config
from core.config import _is_testbed
from flask import Flask, jsonify
from flask import request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

app.config.update(DEBUG=(not _is_app_spot() or _is_testbed()))

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
    """
    here we validate every request in which the frontend uses the google sign-in API to generate the token.
    each request should have "google_id_token" on the header with a valid value from the google api.

    set CLIENT_AUTH_ENABLED to 'false' in the configuration file to disable the authentication check
    """
    validate(request)


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
