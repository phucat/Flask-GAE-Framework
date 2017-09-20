import base64
import json

from googleapiclient import discovery

from oauth2client.client import GoogleCredentials

class PubSubService(object):

    _service = None

    def __init__(self, topic, queue_name=None):
        self.topic_name = topic
        self.queue_name = queue_name
        self._create_pubsub_service()

    def _create_pubsub_service(self):
        if self._service is None:
            credentials = GoogleCredentials.get_application_default()
            self._service = discovery.build('pubsub', 'v1', credentials=credentials)

        return self._service

    def publish(self, data, attributes):
        service = self._create_pubsub_service()
        data = base64.b64encode(json.dumps(data))
        body = dict()

        body["messages"] = [{"data": data}]

        if attributes:
            body["messages"][0]['attributes'] = attributes
        resp = service.projects().topics().publish(topic=self.topic_name, body=body).execute()
        return resp