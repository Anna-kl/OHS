from app import db
from models.classifiers.classifier import Classifier


def get_classifier(value):
    classifier = db.session.query(Classifier).filter(Classifier.id == value)
    if classifier is None:
        return False
    return True


def validate_classifier_vf(vf):
    if db.session.query(Classifier).filter(Classifier.id == vf.nssd_id).first() is None:
        return False
    if db.session.query(Classifier).filter(Classifier.id == vf.af_sort_id).first() is None:
        return False
    if db.session.query(Classifier).filter(Classifier.id == vf.af_family_id).first() is None:
        return False
    return True
