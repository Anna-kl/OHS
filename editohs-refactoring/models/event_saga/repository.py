from app import db
from enums.status_operation import StatusOperation
from models.event_saga.events_saga import EventSaga
from models.events.event import Event


def save_event_saga(event_saga):
    db.session.add(event_saga)
    db.session.commit()
    return event_saga


def check_event(event):
    current_event = db.session.query(Event).filter(Event.id == event.id).first()
    if current_event is None:
        return False
    else:
        return True


def get_event_after(date_change, type_of_object):
    return db.session.query(EventSaga).filter(EventSaga.date_create > date_change) \
        .filter(EventSaga.status == StatusOperation.COMMIT) \
        .filter(EventSaga.type_of_object == type_of_object) \
        .all()


def find_event(event):
    return db.session.query(EventSaga).filter(EventSaga.event_id == event.event_id).first()


def get_last_event_for_param_by_uuid(date_start, date_end, object_id):
    return db.session.query(EventSaga).filter(EventSaga.date_create > date_start) \
        .filter(EventSaga.date_create < date_end) \
        .filter(EventSaga.status == StatusOperation.COMMIT) \
        .filter(EventSaga.object_id == object_id) \
        .all()


def get_last_event_for_param(date_start, date_end):
    return db.session.query(EventSaga).filter(EventSaga.date_create > date_start) \
        .filter(EventSaga.date_create < date_end) \
        .filter(EventSaga.status == StatusOperation.COMMIT) \
        .all()


def get_events_by_uuid_from_saga(object_id):
    return db.session.query(EventSaga).filter(EventSaga.object_id == object_id) \
        .filter(EventSaga.status == StatusOperation.COMMIT) \
        .all()


def get_events_by_from_saga():
    return db.session.query(EventSaga) \
        .filter(EventSaga.status == StatusOperation.COMMIT) \
        .all()
