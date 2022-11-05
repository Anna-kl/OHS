from enums.type_of_object import TypeOfObject
from models.event_saga.repository import get_events_by_uuid_from_saga, get_events_by_from_saga
from services.classes.event_load_classes import EventLoadVf


def create_services_for_load(data_json, type_of_object):
    type_of_object = TypeOfObject[type_of_object.upper()]
    return EventLoadVf(data_json, type_of_object)


def create_services_for_load_by_uuid(data_json, type_of_object, ):
    type_of_object = TypeOfObject[type_of_object.upper()]
    return EventLoadVf(data_json, type_of_object)


def get_events_by_uuid(data_json, type_of_object, object_id):
    events = get_events_by_uuid_from_saga(object_id)
    return list(map(lambda x: {
        'data': x.data,
        'operation': x.type_of_operation.name
    }, events))


def get_events_all(data_json, type_of_object):
    events = get_events_by_from_saga()
    return list(map(lambda x: {
        'data': x.data,
        'operation': x.type_of_operation.name
    }, events))
