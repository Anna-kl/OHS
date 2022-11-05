from sqlalchemy import Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import desc

from models.event_saga.events_saga import EventSaga

from app import db
from enums.type_of_object import TypeOfObject
from datetime import datetime


class Snapshot(db.Model):
    __tablename__ = "snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    object_id = Column(UUID(as_uuid=True), nullable=True)
    data = Column(String)
    type_of_object = Column(Enum(TypeOfObject), nullable=False)
    date_change = Column(DateTime(True))
    # на какую запись создался snapshot
    event_id = Column(UUID(as_uuid=True), ForeignKey("events_saga.id"), nullable=True)

    def __init__(self, name, object_id, data, type_of_object, event_saga):
        self.name = name
        self.object_id = object_id
        self.data = data
        self.date_change = datetime.now()
        self.type_of_object = type_of_object
        self.event_id = event_saga


    # @classmethod
    # def get_last_snapshot(cls, object_id, type_of_object, date_change):
    #     snapshot = db.session.query(Snapshot).filter(Snapshot.type_of_object == type_of_object) \
    #         .filter(Snapshot.object_id == object_id) \
    #         .filter(Snapshot.dttm_change < date_change) \
    #         .order_by(desc(Snapshot.dttm_change)).first()
    #     if snapshot is None:
    #         snapshot = db.session.query(Snapshot).filter(Snapshot.object_id == object_id).order_by(
    #             desc(Snapshot.dttm_change)).first()
    #     return snapshot
    #
    # @classmethod
    # def find_snapshot(self, type_of_object, root):
    #     return db.session.query(EventSaga).join(Snapshot).filter(Snapshot.type_of_object == type_of_object).filter(
    #         Snapshot.object_id == root.id) \
    #         .order_by(desc(Snapshot.dttm_change)).first()

