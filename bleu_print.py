from flask import Blueprint, request, jsonify
from bcns_logique import create_user, list_users, get_user_by_email, login_user

bp = Blueprint('bp', __name__)

@bp.route('/')
def home():
    return "this is my api"

@bp.route('/users', methods=['POST'])
def create_user_route():
    data = request.json
    resp, code = create_user(data)
    return jsonify(resp), code

@bp.route('/users', methods=['GET'])
def list_users_route():
    return jsonify(list_users())

@bp.route('/users/email/<email>', methods=['GET'])
def get_user_by_email_route(email):
    resp, code = get_user_by_email(email)
    return jsonify(resp), code

@bp.route('/login', methods=['POST'])
def login_user_route():
    data = request.json
    resp, code = login_user(data)
    return jsonify(resp), code