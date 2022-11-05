from flask import Blueprint, jsonify

from backend.errors import BadRequestError
from backend.idm.common import service
from backend.security.settings.service import get_settings_by_key

idm = Blueprint("commands", __name__)


@commands.route('/v1/<type_of_object>/command', methods=['POST'])
def add_object(type_of_object):
    data_from_request = request.get_json()
    command_service = CommandService().validate_json(data_from_request, type_of_object)
    command_service.create_event()
    return jsonify({'message': 'Событие создано', 'code': 201})
