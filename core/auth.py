import logging

from app.exceptions import ForbiddenException
from core.config import Config
from oauth2client import client, crypt

"""
here we validate every request where the frontend uses the google sign-in API to generate the token.
each request should have "google_id_token" on the header or in cookie with a valid value from the google api.

set CLIENT_AUTH_ENABLED to 'false' in the configuration file to disable the authentication check
"""


def validate(request):

    if str(Config.get('CLIENT_AUTH_ENABLED')) == 'True':

        token = request.headers.get('google_id_token')
        client_id = Config.get('ALLOWED_CLIENT_ID')

        if token is None:
            if 'google_id_token' not in request.cookies:
                raise ForbiddenException()

            token = request.cookies.get("google_id_token")

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