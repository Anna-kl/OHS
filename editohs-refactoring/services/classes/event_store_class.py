import abc
import json
from abc import ABC

from attr import define, field

from enums.status_operation import StatusOperation
from enums.type_of_operation import TypeOfOperation
from models.classifiers.repository import validate_classifier_vf
from models.event_create.event_create import EventCreate
from models.event_saga.events_saga import EventSaga
from models.event_saga.repository import find_event, save_event_saga
from models.snapshots.repository import save_snapshot, is_need_create
from models.snapshots.snapshot import Snapshot
from models.vf.armed_force import ArmedForce
from models.vf.repository import get_all_vf, save_vf, update_vf, delete_vf
from services.classes.validation import validate_insert, validate_update, validate_delete


@define
class EventStore(metaclass=abc.ABCMeta):
    data: object
    event: EventCreate
    error_flag = False
    error_message = ''

    def __attrs_post_init__(self):
        self.event = EventCreate(**self.event)

    def event_valid(self):
        event = find_event(self.event)
        if event is None:
            return True
        raise ValueError('Такое событие уже было в системе')

    def create_event_saga(self, object_id, status):
        event_saga = EventSaga(self.event, object_id, status)
        return save_event_saga(event_saga)

    @abc.abstractmethod
    def process(self):
        pass

    def save_saga(self, object_id):
        if self.data is None and object_id is None:
            self.error_flag = True
            self.error_message = 'Такой объект уже есть'
            return None
        if self.data is None:
            saga = self.create_event_saga(object_id, StatusOperation.ERROR)
        else:
            saga = self.create_event_saga(self.data.id, StatusOperation.COMMIT)
        return saga.id

    @abc.abstractmethod
    def save_snapshot(self, saga_id):
        pass

    def create_snapshot(self, saga_id):
        if is_need_create(self.event.type_of_object):
            self.save_snapshot(saga_id)


class EventStoreVf(EventStore, ABC):
    data: ArmedForce
    event: EventCreate

    def get_error(self):
        return self.error_flag

    def process(self):
        saga_id = None
        if self.event_valid():
            if self.event.type_of_operation == TypeOfOperation.ADD:
                saga_id = self.insert()
            elif self.event.type_of_operation == TypeOfOperation.UPDATE:
                saga_id = self.update()
            elif self.event.type_of_operation == TypeOfOperation.DELETE:
                saga_id = self.delete()
        self.create_snapshot(saga_id)
        return self

    def delete(self):
        self.error_flag, self.error_message = validate_delete(self.data)
        if self.error_flag is False:
            delete_vf(self.data)
            return self.save_saga(self.data.id)

    def save_snapshot(self, saga_id):
        snapshot = None
        all_record = get_all_vf()
        all_record = list(map(lambda x: x.to_JSON(), all_record))
        if len(all_record) > 0:
            snapshot = Snapshot(name='snapshot', object_id=None,
                                data=json.dumps(all_record, sort_keys=False,
                                                indent=4,
                                                ensure_ascii=False,
                                                separators=(',', ': ')),
                                type_of_object=self.event.type_of_object, event_saga=saga_id)
            snapshot = save_snapshot(snapshot)
        return snapshot

    def update(self):
        self.error_flag, self.error_message = validate_update(self.data)
        if self.error_flag is False:
            self.data = update_vf(self.data)
            return self.save_saga(self.data.id)

    def insert(self):
        self.error_flag, self.error_message = validate_insert(self.data)
        if self.error_flag is False:
            object_id = self.data.id
            self.data = save_vf(self.data)
            return self.save_saga(object_id)
        return None

