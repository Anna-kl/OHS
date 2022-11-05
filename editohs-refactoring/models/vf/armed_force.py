from datetime import datetime

from sqlalchemy import Column, Integer, text, String, DateTime, create_engine, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app import db
from enums.status_record import StatusRecord
from models.classifiers.repository import get_classifier


class ArmedForce(db.Model):
    __tablename__ = "armed_force"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_id = Column(
        ForeignKey("armed_force.id", ondelete="CASCADE"),
        comment="Идентификатор родительского ВФ", nullable=True
    )
    name = Column(String, comment="Название", nullable=False)
    nssd_id = Column(
        ForeignKey("classifiers.id"),
        nullable=False,
        comment="Идентификатор структурного подразделения",
    )
    af_sort_id = Column(
        ForeignKey("classifiers.id"),
        nullable=False,
        comment="Идентификатор вида ВС",
    )
    af_family_id = Column(
        ForeignKey("classifiers.id"),
        nullable=False,
        comment="Идентификатор рода ВС",
    )
    status = Column(Enum(StatusRecord), nullable=False)
    date_create = Column(DateTime(True), nullable=False)

    def __init__(self, name, parent_id, nssd_id, af_sort_id, af_family_id, id):
        self.name = name
        self.status = StatusRecord.ACTIVE
        self.parent_id = self._validate_uuid(parent_id)
        self.nssd_id = self._validate_classifier(nssd_id)
        self.af_sort_id = self._validate_classifier(af_sort_id)
        self.af_family_id = self._validate_classifier(af_family_id)
        self.date_create = datetime.now()
        self.id = self._validate_uuid(id)

    def _is_exist(self):
        if self.parent_id is None:
            return None
        if self.get_vf_from_id(self.parent_id) is None:
            raise ValueError('Узел родителя не обнаружен')
        else:
            return self.parent_id

    def _validate_classifier(self, classifier):
        if get_classifier(classifier) is False:
            raise ValueError('Нужный классификатор не обнаружен')
        return classifier

    def update(self, new_value):
        self.name = new_value.name
        self.status = new_value.status
        self.parent_id = new_value.parent_id
        self.nssd_id = new_value.nssd_id
        self.af_sort_id = new_value.af_sort_id
        self.af_family_id = new_value.af_family_id
        self.date_create = datetime.now()
        return self

    @classmethod
    def get_vf_by_id(cls, vf_id):
        return db.session.query(ArmedForce).filter(ArmedForce.id == vf_id).first()

    @classmethod
    def get_ch_by_id(cls, vf_id):
        return db.session.query(ArmedForce).filter(ArmedForce.parent_id == vf_id).all()

    def to_JSON(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'status': self.status.name,
            'parent_id': str(self.parent_id),
            'nssd_id': str(self.nssd_id),
            'af_sort_id': str(self.af_sort_id),
            'af_family_id': str(self.af_family_id),
            'date_create': str(self.date_create)
        }

    @classmethod
    def recursive_vf(cls, new_value, root):
        if new_value.parent_id is None:
            return False
        new_value = cls.get_vf_by_id(new_value.parent_id)
        if new_value.parent_id == root.id:
            return True
        else:
            return cls.recursive_vf(new_value, root)

    def validate_parent(self, edit_vf):
        root = self.get_vf_by_id(edit_vf.id)
        if root.parent_id == edit_vf.parent_id:
            return False
        else:
            return self.recursive_vf(edit_vf, self)

    def _validate_uuid(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            return uuid.UUID(value)
        else:
            return value