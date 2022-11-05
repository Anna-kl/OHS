from app import db


def event_save(event):
    db.session.add(event)
    db.session.commit()
    return event


