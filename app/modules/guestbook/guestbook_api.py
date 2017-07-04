from flask import request

from app.modules.guestbook.guestbook_model import GuestBookModel, AddressModel
from core.search import apply_search
from core.utils import create_json_response, ok
from flask import Blueprint

guestbook = Blueprint('guestbook', __name__, url_prefix='/api/guestbook')
apply_search(blueprint=guestbook, model=GuestBookModel, fields=['name'])


@guestbook.route('/', methods=['GET'])
def api_list():
    return create_json_response(GuestBookModel.get_all())


@guestbook.route('/create', methods=['POST'])
def api_create():
    _json = request.get_json()
    email = _json.get('email')
    gb = GuestBookModel.create(email)

    """
    sample of parent to child entity relationship where guestbook is parent and addressbook is child
    """
    AddressModel.add(gb.key, 'test1')
    AddressModel.add(gb.key, 'test2')
    AddressModel.add(gb.key, 'test3')

    return create_json_response(gb)


@guestbook.route('/addressbook/get/<guestbook_key>', methods=['GET'])
def api_addressbook_get(guestbook_key):
    ab =AddressModel.get_address_by_key(guestbook_key)

    return create_json_response(ab)
