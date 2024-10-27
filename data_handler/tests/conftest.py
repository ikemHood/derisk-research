"""
This module contains the fixtures for the tests.
"""

from unittest.mock import MagicMock

import pytest
from data_handler.db.crud import DBConnector, InitializerDBConnector


@pytest.fixture(scope="module")
def mock_db_connector() -> None:
    """
    Mock DBConnector
    :return: None
    """
    mock_connector = MagicMock(spec=DBConnector)
    yield mock_connector


@pytest.fixture(scope="module")
def mock_initializer_db_connector() -> None:
    """
    Mock for InitializerDBConnector
    :return: None
    """
    mock_initializer_connector = MagicMock(spec=InitializerDBConnector)
    yield mock_initializer_connector
