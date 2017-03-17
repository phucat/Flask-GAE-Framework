from google.appengine.ext import ndb
from core.ndb import BasicModel


class GuestBookModel(BasicModel):
    name = ndb.StringProperty(required=True)

    @classmethod
    def get_all(cls):
        return cls.query().fetch()

    @classmethod
    def create(cls, email):
        gb = GuestBookModel()
        gb.name = email
        gb.put()
        return gb