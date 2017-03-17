from google.appengine.ext import ndb
from core.ndb import BasicModel


class GuestBookModel(BasicModel):
    name = ndb.StringProperty(required=True)

    @classmethod
    def get_all(cls):
        return cls.query().fetch()
