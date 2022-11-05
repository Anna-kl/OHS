import functools

from models.classifiers.repository import validate_classifier_vf
from models.vf.armed_force import ArmedForce
from models.vf.repository import get_vf_by_name


# валидация вставки
@functools.singledispatch
def validate_insert(arg):
    raise NotImplementedError


@validate_insert.register
def _insert(arg: ArmedForce):
    if validate_classifier_vf(arg) is False:
        return True, 'Классификатора с таким id нет'
    elif get_vf_by_name(arg.name) is not None:
        return True, 'Такой объект уже есть'
    return False, ''


# валидация изменений
@functools.singledispatch
def validate_update(arg):
    raise NotImplementedError


@validate_update.register
def _update(arg: ArmedForce):
    if validate_classifier_vf(arg) is False:
        return True, 'Классификатора с таким id нет'
    elif arg.validate_parent(arg):
        return True, 'Нельзя установить этого родителя'
    elif arg.get_vf_by_id(arg.id) is None:
        return True, 'Объекта с таким id нет'
    return False, ''


# валидация удаления
@functools.singledispatch
def validate_delete(arg):
    raise NotImplementedError


@validate_delete.register
def _delete(arg: ArmedForce):
    if arg.get_vf_by_id(arg.id) is None:
        return True, 'Объекта с таким id нет'
    return False, ''
