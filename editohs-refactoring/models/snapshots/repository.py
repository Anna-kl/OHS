from sqlalchemy import desc

from app import db
from models.event_saga.repository import get_event_after
from models.snapshots.snapshot import Snapshot


def save_snapshot(snapshot):
    db.session.add(snapshot)
    db.session.commit()
    return snapshot


def get_snapshot_after(date):
    return db.session.query(Snapshot).filter(Snapshot.date_change >= date).order_by(Snapshot.date_change).first()


def get_snapshot_before(date):
    return db.session.query(Snapshot).filter(Snapshot.date_change <= date).order_by(desc(Snapshot.date_change)).first()


def is_need_create(type_of_object):
    snapshot = db.session.query(Snapshot).filter(Snapshot.type_of_object == type_of_object) \
        .order_by(desc(Snapshot.date_change)).first()
    if snapshot is not None:
        last_event = get_event_after(snapshot.date_change, type_of_object)
        if len(last_event) > 5:
            return True
    else:
        return True
    return False
