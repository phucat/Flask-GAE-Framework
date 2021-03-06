from app.components.calendar import CalendarService
from app.components.cloud_storage import CloudStorageService
from app.components.pubsub import PubSubService
from core.config import Config
from core.utils import create_json_response, ok
from flask import Blueprint


gcloud = Blueprint('storage', __name__, url_prefix='/api/gcloud')
pubsub_service = PubSubService(topic=Config.get('PUBSUB_TOPIC'))


@gcloud.route('/', methods=['GET'])
def api_index():
    return "see this source code for the sample implementation of storage, pubsub and calendar API ... "


@gcloud.route('/storage/<content>/<filename>', methods=['GET'])
def api_storage(content, filename):

    response = {
        'path': CloudStorageService.upload(content, filename)
    }
    return create_json_response(response)


@gcloud.route('/pubsub/publish', methods=['GET'])
def api_pubsub():
    data = {
        'test': "test"
    }
    pubsub_service.publish(data, {'message_type': 'INFO'})
    return "If successful, you should be able to see a new log on the cloud console"


@gcloud.route('/calendar/list', methods=['GET'])
def api_calendar():
    email = "ray.tenorio@sherpatest.com"
    calendar_events = CalendarService.get_events(email)
    return create_json_response(calendar_events)
