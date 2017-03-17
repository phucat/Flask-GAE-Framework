import logging
from google.appengine.api import urlfetch


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
        logging.exception('Caught exception fetching url')
        raise e