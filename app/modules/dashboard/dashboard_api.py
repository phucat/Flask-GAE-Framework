from flask import Blueprint
from flask import request
from flask_cors import cross_origin

dashboard = Blueprint('dashboard', __name__, url_prefix='/api/dashboard')


@dashboard.route('/test', methods=['POST'])
@cross_origin()
def api_hello():
    data = "Received aPOST body raw content => " + request.get_data()

    return data, 200

