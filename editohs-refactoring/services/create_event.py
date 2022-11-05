import json
from os import environ

import requests

from enums.type_of_object import TypeOfObject
from enums.type_of_operation import TypeOfOperation
from models.event_create.event_create import EventCreate


def parse_json(data_json):
    type_of_operation = data_json['type_of_operation']
    data = data_json['data']
    object_id = data_json['object_id']
    return type_of_operation, data, object_id


def create_event(data_json,type_of_object):
    type_of_operation, data, object_id = parse_json(data_json)
    data = json.dumps(data, sort_keys=False,
                      indent=4,
                      ensure_ascii=False,
                      separators=(',', ': '))
    try:
        type_of_operation = TypeOfOperation[type_of_operation]
        type_of_object = TypeOfObject[type_of_object.upper()]
    except Exception as ex:
        raise TypeError('Типы указаны неверное')
    event_create = EventCreate(type_of_operation, data, type_of_object)

    translate_event(event_create)


def translate_event(event):
    hosts = json.loads(environ.get('hosts'))
    headers = {"Content-Type": "application/json; charset=utf-8"}
    for host in hosts:
        response = requests.post('{}/events'.format(host), headers=headers, data=json.dumps(event.to_json()))
        # if response.status_code == 200:
        #     print(json.loads(response.text))

