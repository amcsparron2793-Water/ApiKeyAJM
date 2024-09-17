# Project Name

This project provides a class for managing and retrieving API keys. It is designed to be flexible and easily integrated into various applications, with optional support for custom logging.

## Features

- Provides a way to read and manage API keys
- Optional logging support
- Configurable API key location

## Requirements

- Python 3.12.2
- [pip](https://pip.pypa.io/en/stable/)

## Installation

To install the necessary dependencies, run:

```bash
pip install -r requirements.txt
```

_Note: Ensure Python 3.12.2 is installed on your system._

## Usage

To use the `APIKey` class, you can follow the example below:

```python
from path.to.api_key_module import APIKey

# Example usage
apiKey = APIKey(logger=myLogger, api_key_location='path/to/api_key.txt')
key = apiKey.api_key
```

### Example Description

The above example shows how to instantiate the `APIKey` class using optional parameters such as `logger` and `api_key_location`. The `api_key` property can then be accessed to retrieve the key.

## Class and Methods Description

### `APIKey`

The `APIKey` class provides a way to read and manage API keys.

#### Methods:

- `__init__(self, **kwargs)`: 
  Initializes an instance of the `APIKey` class. Parameters include:
  - `logger`: The logger for logging messages.
  - `api_key`: The API key to be used.
  - `api_key_location`: The location of the file containing the API key.

- `API_KEY(cls, **kwargs)`:
  A class method that returns an instance of the `APIKey` class with the provided keyword arguments. Returns the `api_key` property of the created instance.

- `_key_file_not_found_error(self)`:
  A private method that raises a `FileNotFoundError` with a specified error message when the key file is not found.

- `_get_api_key(self, key_location: Optional[Union[Path, str]] = None)`:
  A private method that retrieves the API key from the specified location. If `key_location` is not provided, it uses the `api_key_location` property of the instance. It reads the key from the file and sets it as the `api_key` property of the instance. Raises appropriate exceptions if the file is not found or there is an IOError.

### Properties:

- `DEFAULT_KEY_LOCATION`: The default location of the API key file. Can be set to a specific path.

## Note:

- It is recommended to provide a custom logger for logging purposes.
- The `APIKey` class must be instantiated before accessing the `api_key` property.

## Contribution

Feel free to contribute to this project by creating issues or submitting pull requests. Please follow the [contribution guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to reach out for any questions or issues regarding the usage of this project!