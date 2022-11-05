from flask import Blueprint, jsonify

from backend.errors import BadRequestError
from backend.idm.common import service
from backend.security.settings.service import get_settings_by_key

idm = Blueprint("events", __name__)

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
