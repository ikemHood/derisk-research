"""
This module contains the ZklendTransformer class, 
which is used to transform Zklend events.
"""

from pydantic import BaseModel
from data_handler.db.models.base import Base
from handler_tools.api_connector import DeRiskAPIConnector
from typing import Dict, Any, Tuple, Type, Callable
from data_handler.handler_tools.data_parser.serializers import (
    AccumulatorsSyncEventData as AccumulatorsSyncSerializer,
    LiquidationEventData as LiquidationSerializer,
    ZkLendDataParser,
)
from data_handler.db.models.zklend_events import (
    AccumulatorsSyncEventData as AccumulatorsSyncModel,
    LiquidationEventData as LiquidationModel,
)
from data_handler.db.crud import ZkLendEventDBConnector

EVENT_MAPPING: Dict[str, Tuple[Callable, str, Type[Base]]] = {
    "zklend::market::Market::AccumulatorsSync": (
        ZkLendDataParser.parse_accumulators_sync_event,
        "create_accumulator_event",
        AccumulatorsSyncModel
    ),
    "zklend::market::Market::Liquidation": (
        ZkLendDataParser.parse_liquidation_event,
        "create_liquidation_event",
        LiquidationModel
    ),
}

class ZklendTransformer:
    """
    A class that is used to transform Zklend events into database models.
    """

    EVENT_MAPPING: Dict[str, Tuple[Callable, Type[BaseModel], Type[Base]]] = EVENT_MAPPING
    
    def __init__(self):
        self.api_connector = DeRiskAPIConnector()
        self.db_connector = ZkLendEventDBConnector()
    
    def fetch_and_transform_events(self, from_address: str, min_block: int, max_block: int) -> None:
        """
        Fetch events from the DeRisk API and transform them into database models.
        """
        # Fetch events using the API connector
        response = self.api_connector.get_data(
            from_address=from_address,
            min_block_number=min_block,
            max_block_number=max_block
        )

        if "error" in response:
            raise ValueError(f"Error fetching events: {response['error']}")

        # Process each event based on its type
        for event in response:
            event_type = event.get("key_name")
            if event_type in self.EVENT_MAPPING:
                parser_func, method_name, model_class = self.EVENT_MAPPING[event_type]
                parsed_data = parser_func(event["data"])
                db_model = model_class(**parsed_data.model_dump())
                self.db_connector[method_name](db_model)
            else:
                raise ValueError(f"Event type {event_type} not supported, yet...")

    def save_accumulators_sync_event(self, event: Dict[str, Any]) -> None:
        """
        Save an accumulators sync event to the database.
        """
        parser_func, _, model_class = self.EVENT_MAPPING["zklend::market::Market::AccumulatorsSync"]
        parsed_data = parser_func(event)
        db_model = model_class(**parsed_data.model_dump())
        self.db_connector.create_accumulator_event(db_model)

    def save_liquidation_event(self, event: Dict[str, Any]) -> None:
        """
        Save a liquidation event to the database.
        """
        parser_func, _, model_class = self.EVENT_MAPPING["zklend::market::Market::Liquidation"]
        parsed_data = parser_func(event)
        db_model = model_class(**parsed_data.model_dump())
        
        self.db_connector.create_liquidation_event(db_model)


