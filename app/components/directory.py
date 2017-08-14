from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from core.config import Config


class DirectoryService(object):
    service = None

    def __init__(self):
        self.create_service()

    def create_service(self):
        self.service = discovery.build('admin', 'directory_v1', credentials=(
            ServiceAccountCredentials.from_json_keyfile_name(Config.get('CREDENTIALS_FILE_PATH')) \
                .create_scoped(Config.get('SCOPES')).create_delegated(Config.get('DELEGATED_USER'))
        ))

    def get_user_list(self, group_email):
        return self.service.members().list(groupKey=group_email).execute()

    def get_user_details(self, user_email):
        return self.service.users().get(userKey=user_email, projection="full").execute()
