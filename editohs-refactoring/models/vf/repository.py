from datetime import datetime

from app import db
from models.vf.armed_force import ArmedForce


def save_vf(vf):
    current_vf = db.session.query(ArmedForce).filter(ArmedForce.name == vf.name).first()
    if current_vf is None:
        db.session.add(vf)
        db.session.commit()
    else:
        return None
    return vf


def update_vf(vf_new):
    vf = vf_new.get_vf_by_id(vf_new.id)
    vf.update(vf_new)
    db.session.commit()
    return vf


def get_vf_from_id(vf_id):
    return db.session.query(ArmedForce).filter(ArmedForce.id == vf_id).first()


def get_vf_by_name(name):
    return db.session.query(ArmedForce).filter(ArmedForce.name == name).first()


def delete_vf(vf):
    vf = db.session.query(ArmedForce).filter(ArmedForce.id == vf.id).first()
    db.session.delete(vf)
    db.session.commit()


# def update_vf(old_value, new_value):
#     old_value.name = new_value.name
#     old_value.status = new_value.status
#     old_value.parent_id = new_value.parent_id
#     old_value.nssd_id = new_value.nssd_id
#     old_value.af_sort_id = new_value.af_sort_id
#     old_value.af_family_id = new_value.af_family_id
#     old_value.date_create = datetime.now()
#     db.session.commit()
#     return old_value

def get_all_vf():
    vf_all = db.session.query(ArmedForce).all()
    return vf_all
