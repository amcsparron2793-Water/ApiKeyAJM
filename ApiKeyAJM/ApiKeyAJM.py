"""
ApiKeyAJM.py

reusable API key getter

"""

from _version import __version__
from logging import getLogger
from pathlib import Path
from typing import Optional, Union


class APIKey:
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

    def __init__(self, **kwargs):
        if hasattr(self, 'logger'):
            pass
        else:
            self.logger = kwargs.get('logger', getLogger('dummy_logger'))

        self.api_key = kwargs.get('api_key')
        self.api_key_location = kwargs.get('api_key_location')

        if not self.api_key and not self.api_key_location:
            self.api_key_location = self.DEFAULT_KEY_LOCATION
            if not self.api_key_location:
                raise AttributeError('api_key_location not found, is DEFAULT_KEY_LOCATION set correctly?')
        elif not self.api_key:
            self.api_key = self._get_api_key(self.api_key_location)

        self.logger.info(f"{self.__class__.__name__} Initialization complete.")

    @classmethod
    def API_KEY(cls, **kwargs):
        print(kwargs)
        return cls(**kwargs).api_key

    def _key_file_not_found_error(self):
        try:
            raise FileNotFoundError('key file not found')
        except FileNotFoundError as e:
            self.logger.error(e, exc_info=True)
            raise e

    def _get_api_key(self, key_location: Optional[Union[Path, str]] = None):
        if not key_location:
            if self.api_key_location.is_file():
                try:
                    with open(self.api_key_location, 'r') as f:
                        key = f.read().strip()
                except FileNotFoundError as e:
                    self._key_file_not_found_error()
                except IOError as e:
                    self.logger.error(e, exc_info=True)
                    raise e
            else:
                self._key_file_not_found_error()
        else:
            if Path(key_location).is_file():
                with open(key_location, 'r') as f:
                    key = f.read().strip()
            else:
                self._key_file_not_found_error()
        self.api_key = key
        return self.api_key
