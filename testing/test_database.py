from __future__ import annotations

import base64
import logging
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from API.database import Database
from API.route import router
from API.utils import init_logging_config

init_logging_config()


def test_vector_search():
    """
    Test that the vector_search function returns the correct result.
    """

    mock_result = [
        {"Name": "Test1", "Image": "encoded_string1", "score": 0.8},
        {"Name": "Test2", "Image": "encoded_string2", "score": 0.7},
    ]

    mock_vector_search = MagicMock(return_value=mock_result)

    with patch("API.database.Database.vector_search", mock_vector_search):
        embedding = [0.1, 0.2, 0.3]
        result = Database.vector_search("collection_name", embedding)

        assert result == mock_result
        mock_vector_search.assert_called_once_with(
            "collection_name",
            embedding,
        )
