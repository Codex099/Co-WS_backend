from flask import Blueprint, request, jsonify
from bcns_logique import create_user, get_user_by_email, login_user, signup_request, confirm_signup, create_booking, get_available_slots_range, get_all_locations, get_user_by_id, update_user_by_id

bp = Blueprint('bp', __name__)

@bp.route('/')
def home():
    return "this is my api"

@bp.route('/users', methods=['POST'])
def create_user_route():
    data = request.json
    resp, code = create_user(data)
    return jsonify(resp), code

@bp.route('/users/email/<email>', methods=['GET'])
def get_user_by_email_route(email):
    resp, code = get_user_by_email(email)
    return jsonify(resp), code

@bp.route('/login', methods=['POST'])
def login_user_route():
    data = request.json
    resp, code = login_user(data)
    return jsonify(resp), code

@bp.route('/sign-in-request', methods=['POST'])
def sign_in_request_route():
    data = request.json
    resp, code = signup_request(data)
    return jsonify(resp), code

@bp.route('/confirm-sign-in', methods=['POST'])
def confirm_sign_in_route():
    data = request.json
    email = data.get('email')
    code = data.get('code')
    resp, code = confirm_signup(email, code)
    return jsonify(resp), code

@bp.route('/bookings', methods=['POST'])
def create_booking_route():
    data = request.json
    resp, code = create_booking(data)
    return jsonify(resp), code

@bp.route('/rooms/<int:room_id>/slots', methods=['GET'])
def available_slots_range_route(room_id):
    start = request.args.get('start')  # format 'YYYY-MM-DD'
    end = request.args.get('end')      # format 'YYYY-MM-DD'
    resp, code = get_available_slots_range(room_id, start, end)
    return jsonify(resp), code

@bp.route('/locations', methods=['GET'])
def get_all_locations_route():
    resp, code = get_all_locations()
    return jsonify(resp), code

@bp.route('/rooms/by-location/<location_name>', methods=['GET'])
def rooms_by_location_name_route(location_name):
    from bcns_logique import get_rooms_by_location_name
    resp, code = get_rooms_by_location_name(location_name)
    return jsonify(resp), code

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id_route(user_id):
    resp, code = get_user_by_id(user_id)
    return jsonify(resp), code

@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user_by_id_route(user_id):
    data = request.json
    resp, code = update_user_by_id(user_id, data)
    return jsonify(resp), code

@bp.route('/reservations/user/<int:user_id>', methods=['GET'])
def get_user_reservations_route(user_id):
    from bcns_logique import get_user_reservations
    resp, code = get_user_reservations(user_id)
    return jsonify(resp), code


