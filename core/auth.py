import json
import logging
import urllib2

from flask import session

from app.exceptions import ForbiddenException
from core.config import Config
from oauth2client import client, crypt

"""
here we validate every request where the frontend uses the google sign-in API to generate the token.
each request should have "google_id_token" on the header or in cookie with a valid value from the google api.

set CLIENT_AUTH_ENABLED to 'false' in the configuration file to disable the authentication check

TYPES of token allowed:

1. google_id_token = can be provided on Google Sign-In page
2. Authorization Bearer token = can be provided from "gcloud auth application-default print-access-token"                                   

"""


def validate_authentication_header(request):

    allowed_api = Config.get('API_AUTH_EXCEPTION').split(',')
    logging.info(allowed_api)
    logging.info(request.path)

    if str(Config.get('CLIENT_AUTH_ENABLED')) == 'True' and request.path not in allowed_api:

        token = request.headers.get('google-id-token')
        authorization = request.headers.get('Authorization')
        client_id = Config.get('ALLOWED_CLIENT_ID')

        logging.info("google_id_token => " + str(token))
        logging.info("authorization  => " + str(authorization))
        logging.info("ALLOWED_CLIENT_ID => " + client_id)

        if authorization is None and token is None:
            raise ForbiddenException("Forbidden.")

        if token:
            logging.info("token: %s, client_id: %s" % (token, client_id))
            validate_google_id_token(token, client_id)

        elif authorization:
            # authorization
            validate_authentication_token(authorization)
        else:
            raise ForbiddenException("Forbidden.")


def validate_google_id_token(token, client_id):
    try:

        id_info = client.verify_id_token(token, client_id)

        logging.info(id_info)
        logging.info("Domain Check")
        logging.info(Config.get('DOMAIN_CHECK'))

        if Config.get('DOMAIN_CHECK') == 'True':
            if id_info.get('hd') not in Config.get('ALLOWED_DOMAIN').split(', '):
                raise ForbiddenException("Domain not allowed.")

        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ForbiddenException("Domain not allowed")

        session['user_info'] = id_info

    except crypt.AppIdentityError as e:
        # Invalid token
        raise ForbiddenException(e.message)


def validate_authentication_token(access_token):
    try:
        resp = urllib2.urlopen(urllib2.Request("https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=" + access_token[7:],
                                               headers={'Host': 'www.googleapis.com', 'Authorization': access_token}))
        response_code = resp.getcode()
        logging.info("response code : " + str(response_code))

        if not response_code == 200:
            raise ForbiddenException("Error on auth, response code: %s, mesage: %s" % (response_code, resp.read()))
        else:
            data = ""
            for line in resp:
                line_words = line.split("\n")
                data = data + line_words[0]

            logging.info(data)
            return json.loads(data)

    except urllib2.HTTPError as e:
        logging.info("error")
        raise ForbiddenException("Auth Error : " + e.msg)
    except urllib2.URLError as e:
        logging.info(e)
