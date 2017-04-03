from app.components.cloud_storage import CloudStorageService
from core.utils import create_json_response
from flask import Blueprint

storage = Blueprint('storage', __name__, url_prefix='/storage')


@storage.route('/', methods=['GET'])
def api_index():
    return "go to <strong>/storage/[content]/[filename]</strong> to create a sample file in cloudstorage";


@storage.route('/<content>/<filename>', methods=['GET'])
def api_create_file(content, filename):

    response = {
        'path': CloudStorageService.upload(content, filename)
    }
    return create_json_response(response)

