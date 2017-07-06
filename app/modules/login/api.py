import logging
from flask import Blueprint, session

from core.cross_domain import crossdomain
from core.utils import create_json_response

login = Blueprint('login', __name__, url_prefix='/api/login')


@login.route('/me', methods=['GET', 'POST'])
@crossdomain(origin='*')
def api_me():
    logging.info(session.get('user_info'))
    return create_json_response(session.get('user_info'))