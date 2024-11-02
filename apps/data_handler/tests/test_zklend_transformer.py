"""
Test the zklend transformer
"""

import pytest
from unittest.mock import MagicMock
from apps.data_handler.handlers.events.zklend.transform_events import ZklendTransformer


@pytest.mark.asyncio
async def test_zklend_transformer(
    mock_zklend_event_db_connector: MagicMock,
    mock_api_connector: MagicMock,
):
    """
    Test the zklend transformer
    """
    transformer = ZklendTransformer(
        mock_zklend_event_db_connector,
        mock_api_connector,
    )
    pass
