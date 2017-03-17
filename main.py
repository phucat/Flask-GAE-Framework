import logging

from flask import request
from flask_autodoc.autodoc import Autodoc
from flask import Flask, jsonify

from app.exceptions import CustomException
from configurations.config import _is_app_spot

from configurations.config import _is_testbed

app = Flask(__name__)
auto = Autodoc(app)

app.config.update(DEBUG=(not _is_app_spot() or _is_testbed()))


#app.register_blueprint(jml_queue)



@app.before_request
def auth_user():
    logging.info(request.headers)
    """
    executed before entering blueprint endpoints
    """


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
