import logging

from app.exceptions import ForbiddenException
from core.config import Config
from oauth2client import client, crypt


def validate(request):

    if str(Config.get('CLIENT_AUTH_ENABLED')) == 'True':

        token = request.headers.get('google_id_token')
        client_id = Config.get('ALLOWED_CLIENT_ID')

        if token is None:
            raise ForbiddenException()

        try:
            logging.info("token: %s, client_id: %s" % (token, client_id))
            id_info = client.verify_id_token(token, client_id)
            logging.info(id_info)

            if Config.get('DOMAIN_CHECK') is True:
                if id_info.get('hd') not in Config.get('ALLOWED_DOMAIN').split(','):
                    raise ForbiddenException()

            if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ForbiddenException()

        except crypt.AppIdentityError:
            # Invalid token
            raise ForbiddenException()