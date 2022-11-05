import abc
import json
from datetime import datetime

from enums.type_of_object import TypeOfObject
from enums.type_of_operation import TypeOfOperation
from models.classifiers.classifier import Classifier
from models.event_saga.repository import get_last_event_for_param, get_last_event_for_param_by_uuid
from models.snapshots.repository import get_snapshot_before


class ServicesLoadSnapshot(metaclass=abc.ABCMeta):
    error_flag = False
    send_data = []
    with_delete = False

    def __init__(self, args, type_of_object):
        self.snapshot = None
        try:
            self.date_at = datetime.strptime(args['date_at'], '%Y-%m-%d %H:%M:%S')
            self.with_delete = True if args['with_delete'] == 'true' else False
            self.type_of_object = type_of_object
        except Exception as ex:
            self.error_flag = True
            self.error_message = "Не правильный формат запроса"

        if self.error_flag is False:
            if self.type_of_object == TypeOfObject.CLASSIFIER:
                self.object_vf = Classifier.get_from_id(self.object_id)
            # elif self.type_of_object == TypeOfObject.VF:
            #     self.object_vf = ArmedForce
            # if self.object is None:
            #     self.error_flag = True
            #     self.error_message = 'Объекта с таким id нет'
        if self.error_flag is False:
            self.init_snapshot()

    def get_last_event(self):
        last_snapshot = get_snapshot_before(self.date_at)
        if last_snapshot is None:
            self.error_flag = True
            self.error_message = 'В системе нет снимков'
            return None, None
        if self.error_flag is False:
            last_events = get_last_event_for_param(last_snapshot.date_change, self.date_at)
            return last_snapshot, last_events

    def get_last_event_by_uuid(self, object_id):
        last_snapshot = get_snapshot_before(self.date_at)
        if last_snapshot is None:
            self.error_flag = True
            self.error_message = 'В системе нет снимков'
            return None, None
        if self.error_flag is False:
            last_events = get_last_event_for_param_by_uuid(last_snapshot.date_change, self.date_at, object_id)
            return last_snapshot, last_events

    @abc.abstractmethod
    def init_snapshot(self):
        pass

    def restore_event(self, choose_event):
        if self.type_of_object == TypeOfObject.CLASSIFIER:
            snapshot_data = Classifier.load_from_snapshot(self.snapshot.data)
            for event in choose_event:
                self.object = Classifier.get_from_id(event.object_id)
                snapshot_data.insert_root(snapshot_data, self.object)
            snapshot_data.print(snapshot_data, '')


class EventLoadVf(ServicesLoadSnapshot):
    def init_snapshot(self):
        last_snapshot, last_events = self.get_last_event()
        self.send_data = json.loads(last_snapshot.data)
        if self.error_flag is False:
            for event in last_events:
                if event.type_of_operation == TypeOfOperation.ADD:
                    self.send_data.append(json.loads(event.data))
                elif event.type_of_operation == TypeOfOperation.UPDATE:
                    data_from_event = json.loads(event.data)
                    self.send_data = list(filter(lambda x: x['id'] != data_from_event['id'], self.send_data))
                    self.send_data.append(json.loads(event.data))
                elif event.type_of_operation == TypeOfOperation.DELETE:
                    data_from_event = json.loads(event.data)
                    self.send_data = list(filter(lambda x: x['id'] != data_from_event['id'], self.send_data))
                    if self.with_delete:
                        deleted_object = json.loads(event.data)
                        deleted_object['comment'] = TypeOfOperation.DELETE.name
                        self.send_data.append(deleted_object)

        return self.send_data
