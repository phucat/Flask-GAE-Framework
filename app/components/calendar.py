from oauth2client.contrib.appengine import AppAssertionCredentials


class CalendarService(object):

    delegated_credentials = None
    scopes = ()

    def __init__(self, email):
        self.delegate_user = email
        self._create_credentials()

    def _create_credentials(self):

        if self.delegated_credentials is None:
            credentials = AppAssertionCredentials(
                'https://www.googleapis.com/auth/calendar')
            self.delegated_credentials =credentials.create_delegated(self.delegate_user)

        return self.delegated_credentials

    def create_event(self, subject,):
        pass