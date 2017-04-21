from flask import Blueprint

hello_world = Blueprint('hello_world', __name__, url_prefix='/')


@hello_world.route('/', methods=['GET', 'POST'])
def api_hello():
    return "Hello Flask - GAE Boilerplate";

