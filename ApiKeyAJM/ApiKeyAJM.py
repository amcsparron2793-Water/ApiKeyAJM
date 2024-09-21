"""
ApiKeyAJM.py

Provides a way to read/manage API keys.
"""

from logging import getLogger
from pathlib import Path
from typing import Optional, Union
import requests
import validators

class APIKeyBase:
    """
    APIKey is a class that provides a way to read/manage API keys. It has the following methods:
    __init__(self, **kwargs):
        Initializes an instance of the APIKey class. It takes optional keyword arguments:
        - logger: The logger to be used for logging messages. If not provided, a dummy logger will be used.
        - api_key: The API key to be used. If not provided, it will try to get the key from api_key_location.
        - api_key_location: The location of the file containing the API key. If not provided, it will use the DEFAULT_KEY_LOCATION.
    API_KEY(cls, **kwargs):
        This is a class method that returns an instance of the APIKey class with the provided keyword arguments.
        It takes the same keyword arguments as __init__ and returns the api_key property of the created instance.
    _key_file_not_found_error(self):
        This is a private method that raises a FileNotFoundError with a specified error message.
        It is called when the key file is not found.
    _get_api_key(self, key_location: Optional[Union[Path, str]] = None):
        This is a private method that gets the API key from the specified location.
        It takes an optional argument 'key_location' which can be a Path or a string.
        If key_location is not provided, it will use the api_key_location property of the instance.
        If the file is found, it reads the key from the file and sets it as the api_key property of the instance.
        If the file is not found or there is an IOError, it raises the appropriate exception.
    Note:
    - The DEFAULT_KEY_LOCATION property of the APIKey class can be set to the default location of the API key file.
    - The logger property is optional but it is recommended to provide a custom logger for logging purposes.
    - The APIKey class must be instantiated before accessing the api_key property.
    Example Usage:
        apiKey = APIKey(logger=myLogger, api_key_location='path/to/api_key.txt')
        key = apiKey.api_key
    """
    DEFAULT_KEY_LOCATION = None
    DEFAULT_LOGGER_NAME = 'dummy_logger'

    def __init__(self, **kwargs):
        self._is_file_key = kwargs.get('is_file_key', True)
        self._initialize_logger(kwargs.get('logger'))
        self.api_key = kwargs.get('api_key')
        self.api_key_location = kwargs.get('api_key_location')
        if self._is_file_key:
            if not self.api_key:
                self._ensure_key_location_is_set()
                self.api_key = self._fetch_api_key(self.api_key_location)

        self.logger.info(f"{self.__class__.__name__} Initialization complete.")

    def _initialize_logger(self, logger):
        self.logger = logger or getLogger(self.DEFAULT_LOGGER_NAME)

    def _ensure_key_location_is_set(self):
        if not self.api_key_location:
            if not self.DEFAULT_KEY_LOCATION:
                raise AttributeError('api_key_location or api_key were not passed in as kwargs and '
                                     'DEFAULT_KEY_LOCATION not set, is it defined in the class?')
            else:
                self.api_key_location = self.DEFAULT_KEY_LOCATION

    @classmethod
    def get_api_key(cls, **kwargs):
        return cls(**kwargs).api_key

    def _key_file_not_found_error(self):
        try:
            raise FileNotFoundError('key file not found')
        except FileNotFoundError as e:
            self.logger.error(e, exc_info=True)
            raise e

    def _fetch_api_key(self, key_location: Optional[Union[Path, str]] = None):
        if key_location and Path(key_location).is_file():
            key_path = key_location
        elif self.api_key_location and Path(self.api_key_location).is_file():
            key_path = self.api_key_location
        else:
            self._key_file_not_found_error()
            return None

        try:
            with open(key_path, 'r') as f:
                return f.read().strip()
        except IOError as e:
            self.logger.error(e, exc_info=True)
            raise e


class RemoteAPIKey(APIKeyBase):
    IS_FILE_KEY = False
    def __init__(self, base_url: str, create_key_endpoint: str, **kwargs):
        self._base_url = base_url
        self._create_key_endpoint = create_key_endpoint
        self._full_url = self._construct_full_url()

        username = kwargs.get('username')
        password = kwargs.get('password')

        # Inline the logic of assigning api_key
        self.api_key = None if not username or not password else self._fetch_api_key(username, password)

        # super class needs a dummy api_key value
        super().__init__(api_key=self.api_key, is_file_key=self.IS_FILE_KEY, **kwargs)

    def _construct_full_url(self) -> str:
        return f'{self.validated_base_url}/{self._create_key_endpoint}'

    @property
    def validated_base_url(self) -> str:
        if self._base_url and not validators.url(self._base_url):
            raise validators.ValidationError("Invalid URL")
        return self._base_url or None

    # noinspection PyMethodOverriding
    def _fetch_api_key(self, username: str, password: str) -> str:
        try:
            response = requests.post(
                url=self._full_url,
                json={'username': username, 'password': password},
                headers={'Content-Type': 'application/json'}
            )
            if response.ok:
                return response.json()
            else:
                raise requests.exceptions.RequestException(response.text)
        except requests.exceptions.ConnectionError as e:
            raise requests.exceptions.ConnectionError(e) from None

    @classmethod
    def get_api_key(cls, **kwargs):
        if not kwargs.get('username') or not kwargs.get('password'):
            raise AttributeError('username or password were not passed in as kwargs')
        return cls(**kwargs).api_key['api_key']

if __name__ == '__main__':
    # username = 'andrew'
    # password = '<PASSWORD>'

    remote_api_key = RemoteAPIKey(base_url='http://127.0.0.1:5000', create_key_endpoint='get_api_key',
        username='andrew',password='<PASSWORD>')
    # print(remote_api_key.api_key)

