from datetime import datetime

from attr import attrs, attrib

from app import db
from enums.status_of_operation import StatusEvent


@attrs
class EventHandler:
    event_id = attrib()
    object_id = attrib()
    type_of_operation = attrib()
    status = attrib(default=StatusEvent.CREATE)
    date_create = attrib(default=datetime.now())
