import json
from datetime import datetime
from sqlalchemy import Column, text, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app import db
from enums.status_of_operation import StatusEvent
from enums.status_operation import StatusOperation
from enums.type_of_object import TypeOfObject
from enums.type_of_operation import TypeOfOperation

from models.event_handler.event_handler import EventHandler
from models.events.event import Event

class EventSaga(db.Model):
    __tablename__ = "events_saga"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type_of_operation = Column(Enum(TypeOfOperation), nullable=False)
    type_of_object = Column(Enum(TypeOfObject), nullable=False)
    object_id = Column(UUID(as_uuid=True), nullable=True)
    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id"), nullable=True)
    date_create = Column(DateTime(True), server_default=text("now()"))
    data = Column(String, nullable=False)
    status = Column(Enum(StatusOperation), nullable=False)

    def __init__(self, event, object_id, status):
        self.type_of_operation = event.type_of_operation
        self.event_id = event.event_id
        self.date_create = datetime.now()
        self.object_id = object_id
        self.data = self._data_to_json(event.data)
        self.status = status
        self.type_of_object = event.type_of_object

    @classmethod
    def get_history_event(cls, root, snapshot):
        return db.session.query(EventSaga).join(EventHandler).filter(EventHandler.object_id == root.id) \
            .filter(EventSaga.dttm_change > snapshot.dttm_change).all()

    def _data_to_json(self, data):
        if isinstance(data, str) is False:
            return json.dumps(data)
        else:
            return data
