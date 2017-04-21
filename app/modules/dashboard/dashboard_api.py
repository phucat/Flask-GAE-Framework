from flask import Blueprint
from flask import request


dashboard = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@dashboard.route('/test', methods=['POST'])
def api_hello():
    data = "Received    POST body raw content => " + request.get_data()

    return data, 200

