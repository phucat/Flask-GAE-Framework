from core.config import Config
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


class GoogleCredential(object):
    pass


class CalendarService(object):

    _service = None
    scopes = ()

    @classmethod
    def _create_service(cls, email):

        if cls._service is None:
            scopes = ['https://www.googleapis.com/auth/calendar']
            credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials/cs-development-playground.json', scopes)
            delegated_credentials = credentials.create_delegated(email)
            cls._service = discovery.build('calendar', 'v3', credentials=delegated_credentials)

        return cls._service

    @classmethod
    def get_events(cls, email):
        service = cls._create_service(email)
        return service.events().list(calendarId="primary").execute()
