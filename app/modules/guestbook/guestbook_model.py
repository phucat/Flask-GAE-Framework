from google.appengine.ext import ndb

from app.exceptions import EmailAlreadyExistException
from core.ndb import BasicModel


class GuestBookModel(BasicModel):
    name = ndb.StringProperty(required=True)
    age = ndb.StringProperty()

    @classmethod
    def get_all(cls):
        return cls.query().fetch()

    @classmethod
    def create(cls, email):

        if cls.get_by_id(email) is not None:
            raise EmailAlreadyExistException()

        gb = GuestBookModel(id=email)
        gb.name = email
        gb.put()
        return gb


class AddressModel(BasicModel):

    """
    here's a sample ancestor parent-child relationship on NDB.
    """
    street = ndb.StringProperty(required=True)

    @classmethod
    def add(cls, parent_key, street):
        ab = AddressModel(parent=parent_key)
        ab.street = street
        ab.put()

    """
    get all child of parent model Guestbook provided by key
    """
    @classmethod
    def get_address_by_key(cls, parent_key):
        key = ndb.Key(urlsafe=parent_key)
        return cls.query(ancestor=key).order(cls.created)