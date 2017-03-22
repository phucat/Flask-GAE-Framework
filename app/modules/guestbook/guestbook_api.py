from flask import request

from app.modules.guestbook.guestbook_model import GuestBookModel
from core.utils import create_json_response, ok
from flask import Blueprint

guestbook = Blueprint('guestbook', __name__, url_prefix='/api/guestbook')


@guestbook.route('/', methods=['GET'])
def api_list():
    return create_json_response(GuestBookModel.get_all())


@guestbook.route('/create', methods=['POST'])
def api_create():
    _json = request.get_json()
    email = _json.get('email')
    gb = GuestBookModel.create(email)

    return create_json_response(gb)
