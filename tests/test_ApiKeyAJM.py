import os
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from ApiKeyAJM.ApiKeyAJM import APIKeyBase


class TestAPIKey(unittest.TestCase):
    def setUp(self):
        self.default_key_path = "test_key_file.txt"
        self.mock_logger = Mock()

    def test_init_with_api_key(self):
        api_key_value = "test_api_key"
        api_key = APIKeyBase(api_key=api_key_value, logger=self.mock_logger)

        self.assertEqual(api_key.api_key, api_key_value)
        self.mock_logger.info.assert_called_once_with("APIKeyBase Initialization complete.")

    def test_init_without_api_key(self):
        with open(self.default_key_path, 'w') as file:
            file.write("file_api_key")

        APIKeyBase.DEFAULT_KEY_LOCATION = self.default_key_path

        api_key = APIKeyBase(logger=self.mock_logger)

        self.assertEqual(api_key.api_key, "file_api_key")
        os.remove(self.default_key_path)

    def test_get_api_key(self):
        api_key_value = "test_api_key_classmethod"
        api_key_returned = APIKeyBase.get_api_key(api_key=api_key_value, logger=self.mock_logger)

        self.assertEqual(api_key_value, api_key_returned)

    def test_key_file_not_found_error(self):
        with self.assertRaises(FileNotFoundError):
            APIKeyBase(api_key_location="non_existing_file_path", logger=self.mock_logger)

    def test_io_error(self):
        with patch.object(Path, "is_file", return_value=True), patch('builtins.open', side_effect=IOError(
                "IO Error")), self.assertRaises(IOError):
            APIKeyBase(api_key_location="error_raising_file_path", logger=self.mock_logger)


if __name__ == "__main__":
    unittest.main()
