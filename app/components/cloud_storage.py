from core.config import Config
from google.cloud import storage

"""
see here for code reference:
https://cloud.google.com/appengine/docs/flexible/python/using-cloud-storage
"""


class CloudStorageService(object):

    service = None

    def __init__(self):
        self._create_cloud_storage_service()

    @classmethod
    def upload(cls, content, filename):
        gcs = storage.Client()
        bucket = gcs.get_bucket(Config.get('DEFAULT_BUCKET'))
        blob = bucket.blob(filename)

        blob.upload_from_string(
            content,
            content_type="text/plain"
        )

        # The public URL can be used to directly access the uploaded file via HTTP.
        return blob.public_url
