import collections
import json

import datetime
import logging

from google.appengine.api import users, urlfetch

from core.config import _is_app_spot, _is_testbed, Config
from flask import request, Response, g
from oauth2client import client, crypt

urlfetch.set_default_fetch_deadline(60)


def get_current_user_email():
    if _is_app_spot() or _is_testbed():
        return getattr(g, '_current_user_email', None)
    else:
        return users.get_current_user().email()


def set_current_user_email(user_email):
    g._current_user_email = user_email


def create_json_response(response, status=200):
    return Response(response=json.dumps(response), status=status, mimetype='application/json')


def str_to_date(date_as_string):

    return datetime.datetime.strptime(date_as_string, Config.get('DATE_FORMAT')).date()


def json_serial(date):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(date, datetime.date):
        serial = date.strftime(Config.get('DATE_FORMAT'))
        return serial
    raise TypeError("Type not serializable")


def precondition_failed():
    return 'Precondition Failed', 412


def unauthorized():
    return 'Unauthorized', 401


def forbidden():
    return 'Forbidden', 403


def no_content():
    return Response(response='', status=204, content_type=None, headers={}, mimetype=None)


def not_found():
    return 'Not Found', 404


def success_response():
    return 'Success', 200


def ok():
    return 'OK', 200


def verify_token(token):
    id_info = client.verify_id_token(token, None)

    # If multiple clients access the backend server:
    if id_info['aud'] not in Config.get('OAUTH_CLIENT_ID'):
        raise crypt.AppIdentityError("Unrecognized client.")
    if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
        raise crypt.AppIdentityError("Wrong issuer.")
    if id_info['hd'] != Config.get('APPS_DOMAIN_NAME'):
        raise crypt.AppIdentityError("Wrong hosted domain.")

    return id_info


def is_sequence(obj):
    if isinstance(obj, basestring):
        return False
    return isinstance(obj, collections.Sequence)


def appengine_inbound_appid_header_auth(controller):
    headers = controller.request.headers
    if 'X-Appengine-Inbound-Appid' in headers:
        appengine_header = headers['X-Appengine-Inbound-Appid']
        if appengine_header in Config.get('ALLOWED_APP_ENGINE_IDS'):
            return True
        else:
            return False, 'Unauthorized APP_ID:{0}'.format(appengine_header)
    else:
        return False, 'Missing X-Appengine-Inbound-Appid header'


def appengine_queue_name_header_auth(controller):
    headers = controller.request.headers
    if 'X-AppEngine-QueueName' in headers:
        return True
    else:
        return False, 'Missing X-AppEngine-QueueName header'


def url_fetch_svc(url, payload=None, method=urlfetch.POST):
    '''
    :param url:
    :param payload:
    :param method: POST by default
    :return:
    '''
    try:
        headers = {"Content-Type": "application/json"}
        payload = None if payload is None else json.dumps(payload)
        logging.info("payload : %s" % payload)
        logging.info("request URL : %s" % url)
        return urlfetch.fetch(
            url=url,
            payload=payload,
            method=method,
            headers=headers,
            deadline=60,
            follow_redirects=False)
    except Exception as e:
        # TODO: return an error message on fail, maybe run from a deferred queue ?
        logging.exception('Caught exception fetching url')
        raise e


def url_fetch_svc(url, payload=None, method=urlfetch.POST, follow_redirects=False, deadline=60):

    '''
    :param url:
    :param payload:
    :param method: POST by default
    :param follow_redirects: POST by default
    :param deadline: POST by default
    :return:
    '''

    try:
        headers = {"Content-Type": "application/json"}
        payload = None if payload is None else json.dumps(payload)
        # logging.info("payload : %s" % payload)
        logging.info("request URL : %s" % url)
        logging.info("request method : %s" % method)

        result = urlfetch.fetch(
            url=url,
            payload=payload,
            method=method,
            headers=headers,
            deadline=deadline,
            follow_redirects=follow_redirects)

        logging.info("status code: " + str(result.status_code))
        # logging.info("result content: " + result.content)

        return result

    except Exception as e:
        # TODO: return an error message on fail, maybe run from a deferred queue ?
        logging.exception('Caught exception fetching url')
        raise e