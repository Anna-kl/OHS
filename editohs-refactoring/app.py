import json

from flask import Flask, request, jsonify, Response
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from database import database_url
from enums.type_of_object import TypeOfObject

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from services.create_event import create_event
from services.snapshot_load import create_services_for_load, create_services_for_load_by_uuid, get_events_by_uuid, \
    get_events_all
from services.event_store import load_event

BLUEPRINTS = (commands)

for blueprint in BLUEPRINTS:
    app.register_blueprint(blueprint)


@app.route('/v1/<type_of_object>/command', methods=['POST'])
def add_object(type_of_object):
    data_from_request = request.get_json()
    create_event(data_from_request, type_of_object)

    return jsonify({'message': 'Событие создано', 'code': 201})


@app.route('/v1/events', methods=['POST'])
def request_event():
    data_event = request.get_json()
    event = load_event(data_event)
    status_code = 200 if event.error_flag is False else 500

    return Response(
        event.error_message,
        status=status_code,
        content_type='application/json',
    )


@app.route('/v1/<type_of_object>', methods=['GET'])
def load_from_snapshot(type_of_object):
    services = create_services_for_load(request.args, type_of_object)

    if services.error_flag:
        return jsonify({'message': services.error_message, 'code': 500})
    return jsonify({'data': services.send_data, 'code': 200})


@app.route('/v1/<type_of_object>/<uuid_object>', methods=['GET'])
def load_from_snapshot_object(type_of_object, uuid_object):
    services = create_services_for_load_by_uuid(request.args, type_of_object, uuid_object)

    if services.error_flag:
        return jsonify({'message': services.error_message, 'code': 500})
    return jsonify({'data': services.send_data, 'code': 200})


@app.route('/v1/<type_of_object>/<uuid_object>/events', methods=['GET'])
def load_events_by_uuid(type_of_object, uuid_object):
    services = get_events_by_uuid(request.args, type_of_object, uuid_object)

    return jsonify({'data': services, 'code': 200})


@app.route('/v1/<type_of_object>/events', methods=['GET'])
def load_events_all(type_of_object):
    services = get_events_all(request.args, type_of_object)

    return jsonify({'data': services, 'code': 200})


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
