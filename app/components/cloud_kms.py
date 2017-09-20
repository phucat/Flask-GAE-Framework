"""
author: Ray
USAGE:
cloudKMSService = CloudKMSService(
    project_id=Config.get('PROJECT_ID'),
    keyring=Config.get('KMS_KEYRING_NAME'),
    cryptokey=Config.get('KMS_CRYPTO_KEY_NAME')
)

cloudKMSService.encrypt('This is a test message')

"""
import base64
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


class CloudKMSService(object):

    project_id = None
    location = None
    keyring = None
    service = None
    block_size = 16

    def __init__(self, project_id='', keyring='', cryptokey='', location='global' ):
        self.project_id = project_id
        self.location = location
        self.keyring = keyring
        self.cryptokey = cryptokey
        self.create_service()

    def create_service(self):
        credentials = GoogleCredentials.get_application_default()
        self.service = discovery.build('cloudkms', 'v1', credentials=credentials)

    def create_keyring(self):
        """Creates a KeyRing in the given location (e.g. global)."""

        # Creates an API client for the KMS API.

        # The resource name of the location associated with the KeyRing.
        parent = 'projects/{}/locations/{}'.format(self.project_id, self.location)

        # Create KeyRing
        request = self.service.projects().locations().keyRings().create(
            parent=parent, body={}, keyRingId=self.keyring)
        response = request.execute()

        return response['name']

    def create_cryptokey(self):
        """Creates a CryptoKey within a KeyRing in the given location."""

        # The resource name of the KeyRing associated with the CryptoKey.
        parent = 'projects/{}/locations/{}/keyRings/{}'.format(
            self.project_id, self.location, self.keyring)

        # Create a CryptoKey for the given KeyRing.
        request = self.service.projects().locations().keyRings().cryptoKeys().create(
            parent=parent, body={'purpose': 'ENCRYPT_DECRYPT'},
            cryptoKeyId=self.cryptokey)
        response = request.execute()

        return response['name']

    def encrypt(self, plain_text):
        """Encrypts data from a plaintext_file_name using the provided CryptoKey
        and saves it to an encrypted_file_name so it can only be recovered with a
        call to decrypt."""

        encoded_text = base64.b64encode(plain_text)

        # The resource name of the CryptoKey.
        name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
            self.project_id, self.location, self.keyring, self.cryptokey)

        # Use the KMS API to encrypt the text.
        cryptokeys = self.service.projects().locations().keyRings().cryptoKeys()
        request = cryptokeys.encrypt(
            name=name, body={'plaintext': encoded_text.decode('utf-8')})
        response = request.execute()
        return response['ciphertext'].encode('utf-8')

    def decrypt(self, cipher_text):
        """Decrypts data from encrypted_file_name that was previously encrypted
        using the CryptoKey with a call to encrypt. Outputs decrypted data to
        decrpyted_file_name."""

        # The resource name of the CryptoKey.
        name = 'projects/{}/locations/{}/keyRings/{}/cryptoKeys/{}'.format(
            self.project_id, self.location, self.keyring, self.cryptokey)

        # Use the KMS API to decrypt the text.
        cryptokeys = self.service.projects().locations().keyRings().cryptoKeys()
        request = cryptokeys.decrypt(
            name=name, body={'ciphertext': cipher_text.decode('utf-8')})
        response = request.execute()

        plaintext_encoded = response['plaintext']
        plaintext_decoded = base64.b64decode(plaintext_encoded)
        return plaintext_decoded


