# ApiKeyAJM

Reusable helpers for retrieving and managing API keys in Python applications.

This package provides two small classes:
- APIKeyFromFile — read an API key from a local file (.txt or .json)
- RemoteAPIKey — obtain an API key from a remote HTTP endpoint using username/password

It is framework-agnostic and designed to be easy to drop into scripts, CLIs, or services.

## Overview

- Centralized logic to fetch API keys from common sources (file or remote endpoint)
- Optional logging via standard library logging
- Configurable defaults (e.g., default key file path, file mode for JSON/text)
- Small surface area with clear, unit-tested behavior for file-based usage

## Tech stack

- Language: Python
- Package/build: setuptools (PEP 517 via pyproject.toml)
- Package manager: pip
- Test framework: unittest (stdlib)
- Runtime deps: requests, validators
- Dev/build tools (listed in requirements.txt): build, setuptools, packaging, pyproject_hooks (used for building/publishing, not required at runtime)

## Requirements

- Python 3.12+ (repository currently uses Python 3.12 paths)
- pip

## Installation

Install dependencies for development/usage from a checkout:

- Windows PowerShell
  - python -m venv .venv
  - .venv\Scripts\Activate
  - pip install -r requirements.txt
  - pip install -e .

Notes:
- If installing as a dependency from PyPI is desired, confirm the package and version are published. TODO: Confirm PyPI package name and availability.

## Usage

Import from the top-level package:

```python
from ApiKeyAJM import APIKeyFromFile, RemoteAPIKey
```

### APIKeyFromFile

Read a key from a file.

```python
from ApiKeyAJM import APIKeyFromFile

# simplest: pass the key directly
ak = APIKeyFromFile(api_key="already_have_it")
print(ak.api_key)

# from a text file
ak = APIKeyFromFile(api_key_location="path/to/key.txt")
print(ak.api_key)  # contents of the file, stripped

# from a JSON file containing {"api_key": "..."}
ak = APIKeyFromFile(api_key_location="path/to/key.json")
print(ak.api_key)  # entire JSON if no json_key is provided

# targeting a specific JSON key
ak = APIKeyFromFile(api_key_location="path/to/key.json", json_key="api_key")
print(ak.api_key)  # value under json_key

# override default key location (class-level)
APIKeyFromFile.DEFAULT_KEY_LOCATION = "./my_default_key.txt"
ak = APIKeyFromFile()
print(ak.api_key)

# classmethod helper if you only want the string
key = APIKeyFromFile.get_api_key(api_key_location="./key.txt")
```

Notes:
- file_mode is auto-detected from the file extension (.txt => text, .json => json). You can override with file_mode="text" or "json" if needed.
- Raises FileNotFoundError when the key file cannot be found, and propagates IOError on read issues. See tests for examples.

### RemoteAPIKey

Obtain a key by POSTing username/password to a remote endpoint.

```python
from ApiKeyAJM import RemoteAPIKey

rk = RemoteAPIKey(
    base_url="https://example.com/api",
    create_key_endpoint="v1/create_key",
    username="user1",
    password="s3cr3t",
)
print(rk.api_key)

# Or just get the string
key = RemoteAPIKey.get_api_key(
    base_url="https://example.com/api",
    create_key_endpoint="v1/create_key",
    username="user1",
    password="s3cr3t",
)
```

Behavior:
- Validates base_url via validators.url; raises validators.ValidationError if invalid.
- Sends a JSON payload {"username": ..., "password": ...} to f"{base_url}/{create_key_endpoint}".
- Expects a JSON response. If the response is a dict and contains "api_key", that value is returned; otherwise the JSON body is returned as-is.
- Raises requests.exceptions.RequestException on non-OK responses; raises requests.exceptions.ConnectionError on connection failures.

## Environment variables

- None required by the library. You may choose to manage your own environment variables for key paths or credentials in your application. TODO: Document any project-wide environment conventions if introduced.

## Commands and scripts

Common tasks (from project root):

- Run tests
  - python -m unittest
  - or: python -m unittest discover -s tests -p "test_*.py"

- Build a distribution (PEP 517)
  - python -m build

- Publish to PyPI with Twine (requires credentials)
  - twine upload dist/*
  - Windows helper script: building_script\sdist_and_twine.bat
    - This script builds (python -m build) and uploads via twine upload dist/*.
    - Review the script before use and ensure credentials are configured. TODO: Add guidance for TestPyPI usage.

## Project structure

```
ApiKeyAJM/
├─ ApiKeyAJM/
│  ├─ __init__.py            # Exposes APIKeyFromFile, RemoteAPIKey
│  ├─ _version.py            # __version__
│  └─ api_key_ajm.py         # Implementation
├─ tests/
│  └─ test_ApiKeyAJM.py      # unittest tests for APIKeyFromFile
├─ building_script/
│  └─ sdist_and_twine.bat    # Windows batch for build+upload
├─ requirements.txt          # runtime + build deps
├─ setup.py                  # setuptools metadata
├─ setup.cfg                 # points description to README.md
├─ pyproject.toml            # build-system = setuptools
├─ LICENSE.txt               # MIT License
└─ README.md                 # this file
```

## Running tests

- Ensure dependencies are installed (see Installation), then run:
  - python -m unittest

## Versioning

- Version is defined in ApiKeyAJM/_version.py as __version__.

## License

MIT License. See LICENSE.txt for details.

## Contributing

Issues and pull requests are welcome. Please open an issue to discuss substantial changes first. TODO: Add contribution guidelines if needed.