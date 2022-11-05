import json
from datetime import datetime

from sqlalchemy import Column, Integer, text, String, DateTime, Enum, create_engine
from sqlalchemy.dialects.postgresql import INET
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship

from app import db
from enums.status_of_operation import StatusEvent
from enums.type_of_object import TypeOfObject
from enums.type_of_operation import TypeOfOperation


class Event(db.Model):
    __tablename__ = "events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_of_operation = Column(Enum(TypeOfOperation), nullable=False)
    type_of_object = Column(Enum(TypeOfObject), nullable=False)
    data = Column(String)
    status = Column(Enum(StatusEvent), nullable=False)
    object_id = Column(UUID(as_uuid=True),  nullable=True)
    date_create = Column(DateTime(True), nullable=False)

    def __init__(self, event_create):
        self.type_of_operation = event_create.type_of_operation
        self.type_of_object = event_create.type_of_object
        self.data = self._data_to_json(event_create.data)
        self.status = StatusEvent.CREATE
        self.object_id = event_create.object_id
        self.date_create = datetime.now()

    @classmethod
    def get_event(cls, type_of_operation, type_of_object):
        return db.session.query(Event).filter(Event.type == type_of_operation).filter(
            Event.object == type_of_object).first()

    def _data_to_json(self, data):
        if isinstance(data, str) is False:
            return json.dumps(data)
        else:
            return data