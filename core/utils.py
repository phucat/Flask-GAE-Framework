import json
import logging

from google.appengine.api import users, urlfetch
from core.json_utils import stringify
from flask import request, Response, g


urlfetch.set_default_fetch_deadline(60)


def create_json_response(response, status=200):
    return Response(response=stringify(response), status=status, mimetype='application/json')


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
        logging.info("result content: " + result.content)

        return result

    except Exception as e:
        # TODO: return an error message on fail, maybe run from a deferred queue ?
        logging.exception('Caught exception fetching url')
        raise e