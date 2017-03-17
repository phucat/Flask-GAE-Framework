from google.appengine.ext import ndb

from app.exceptions import EmailAlreadyExistException
from core.ndb import BasicModel


class GuestBookModel(BasicModel):
    name = ndb.StringProperty(required=True)

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