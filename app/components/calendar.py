from core.config import Config
from googleapiclient import discovery
from oauth2client.contrib.appengine import AppAssertionCredentials
from oauth2client.service_account import ServiceAccountCredentials


class GoogleCredential(object):
    pass


class CalendarService(object):

    _service = None
    scopes = ()

    def __init__(self, email):
        self.delegate_user = email
        self._create_service()

    @classmethod
    def _create_service(cls):

        if cls._service is None:
            scopes = ['https://www.googleapis.com/auth/calendar']
            credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials/cs-development-playground.json', scopes)
            delegated_credentials = credentials.create_delegated(Config.get("DELEGATED_USER"))
            cls._service = discovery.build('calendar', 'v3', credentials=delegated_credentials)

        return cls._service

    @classmethod
    def create_event(cls):
        service = cls._create_service()
        return service.calendarList().list().execute()
