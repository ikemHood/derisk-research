from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    UUID, Boolean, Column, DateTime, Float, ForeignKey,
    MetaData, String, JSON, Integer
)
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy_utils import IPAddressType
from sqlalchemy_utils.types.choice import ChoiceType

from utils.values import ProtocolIDs


class Base(DeclarativeBase):
    """
    Base class for ORM models.

    :ivar id: The unique identifier of the entity.
    """

    id: Mapped[UUID] = Column(UUID, default=uuid4, primary_key=True)
    metadata = MetaData()


class NotificationData(Base):
    __tablename__ = "notification"

    created_at = Column(DateTime, default=datetime.now())
    email = Column(String, index=True, unique=True, nullable=False)
    wallet_id = Column(String, nullable=False)
    telegram_id = Column(String, unique=False, nullable=False)
    ip_address = Column(IPAddressType, nullable=False)
    health_ratio_level = Column(Float, nullable=False)
    protocol_id = Column(ChoiceType(ProtocolIDs, impl=String()), nullable=False)


class TelegramLog(Base):
    """
    Represents a log entry for Telegram notifications.

    :ivar sent_at: The timestamp indicating when the message was sent.
    :ivar notification_data_id: The UUID identifying the notification data associated with this log entry.
    :ivar is_succesfully: A boolean indicating whether the message was sent successfully or not.
    :ivar message: The content of the send message being logged.
    """

    __tablename__ = "telegram_log"

    sent_at = Column(DateTime, default=datetime.now(), nullable=False)
    notification_data_id = Column(ForeignKey(NotificationData.id), nullable=False)
    is_succesfully = Column(Boolean, nullable=False)
    message = Column(String, server_default="", default="", nullable=False)


class OrderBookModel(Base):
    """
    Represents an order book entry in the database.
    """
    __tablename__ = "orderbook"

    token_a = Column(String, nullable=False, index=True)
    token_b = Column(String, nullable=False, index=True)
    timestamp = Column(DateTime, nullable=False)
    block = Column(Integer, nullable=False)
    dex = Column(String, nullable=False, index=True)
    asks = Column(JSON, nullable=True)
    bids = Column(JSON, nullable=True)
