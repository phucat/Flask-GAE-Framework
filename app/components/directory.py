from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery
from core.config import Config

_google_directory = discovery.build('admin', 'directory_v1', credentials=(
    ServiceAccountCredentials.from_json_keyfile_name(Config.get('CREDENTIALS_FILE_PATH')) \
        .create_scoped(Config.get('SCOPES')).create_delegated(Config.get('DELEGATED_USER'))
))


def get_user_list(group_email):
    return _google_directory.members().list(groupKey=group_email).execute()


def get_user_details(user_email):
    return _google_directory.users().get(userKey=user_email, projection="full").execute()
