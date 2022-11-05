import uuid

from attr import attrs, attrib, field

from enums.status_of_operation import StatusEvent
from enums.type_of_operation import TypeOfOperation
from enums.type_of_object import TypeOfObject
from attrs import define

from models.events.event import Event
from models.events.repository import event_save


@define
class CommandService:
    type_of_operation: TypeOfOperation
    data: object
    type_of_object: TypeOfObject
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

    @classmethod
    def validate_json(cls, data_json, type_of_object):
        try:
            type_of_operation = TypeOfOperation[data_json['type_of_operation']]
            data = data_json['data']
            type_of_object = TypeOfObject[type_of_object.upper()]
            return type_of_operation, data, type_of_object
        except ValueError:
            return None, None, None

    def create_event(self, data_json, type_of_object):
        self.type_of_operation, self.data, self.type_of_object = self._validate_json(data_json, type_of_object)
        if self.type_of_operation is None or self.data is None:
            self.data = json.dumps(self.data, sort_keys=False,
                                   indent=4,
                                   ensure_ascii=False,
                                   separators=(',', ': '))

            self._translate_event()

    def _translate_event(self):
        hosts = json.loads(environ.get('hosts'))
        headers = {"Content-Type": "application/json; charset=utf-8"}
        for host in hosts:
            requests.post('{}/events'.format(host), headers=headers, data=json.dumps(self.data.to_json()))
