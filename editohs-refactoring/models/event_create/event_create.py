import uuid

from attr import attrs, attrib, field

from enums.status_of_operation import StatusEvent
from enums.type_of_operation import TypeOfOperation
from enums.type_of_object import TypeOfObject
from attrs import define

from models.events.event import Event
from models.events.repository import event_save


@define
class EventCreate:
    type_of_operation: TypeOfOperation
    data: str
    type_of_object: TypeOfObject
    object_id: uuid = field(default=None)
    status: StatusEvent = field(default=StatusEvent.CREATE)
    event_id: uuid = field(default=None)

    def status_change(self, status):
        self.status = status

    def __attrs_post_init__(self):
        if isinstance(self.type_of_object, str):
            self.type_of_object = TypeOfObject[self.type_of_object]
        if isinstance(self.type_of_operation, str):
            self.type_of_operation = TypeOfOperation[self.type_of_operation]
        event = Event(self)
        event = event_save(event)
        self.event_id = event.id

    def to_json(self):
        return {
            'type_of_operation': self.type_of_operation.name,
            'type_of_object': self.type_of_object.name,
            'data': self.data,
            'object_id': self.object_id,
            'status': self.status.name,
            'event_id': str(self.event_id)
        }
