from flask import Blueprint, render_template, request, redirect, url_for
from data_access1 import (
    get_all_users,
    get_all_locations,
    get_all_rooms,
    get_user_by_email,
    get_user_by_id,
    create_user,
    create_location,
    create_room,
    delete_user,
    delete_room,
    get_user_balance,
    get_user_recharges,
)

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')


@admin_bp.route('/')
def admin_home():
    return render_template('home.html')


@admin_bp.route('/users')
def users_page():
    search_email = request.args.get('search_email')
    if search_email:
        users = [get_user_by_email(search_email)] if get_user_by_email(search_email) else []
    else:
        users = get_all_users()
    return render_template('users.html', users=users)


@admin_bp.route('/locations')
def locations_page():
    locations = get_all_locations()
    return render_template('locations.html', locations=locations)


@admin_bp.route('/rooms')
def rooms_page():
    rooms = get_all_rooms()
    locations = get_all_locations()
    return render_template('rooms.html', rooms=rooms, locations=locations)


@admin_bp.route('/users/update_balance/<int:user_id>', methods=['POST'])
def update_balance(user_id):
    amount = float(request.form.get('balance'))
    from data_access1 import create_recharge
    create_recharge({'user_id': user_id, 'amount': amount})
    return redirect(url_for('admin_bp.users_page'))


@admin_bp.route('/users/create', methods=['POST'])
def create_user_admin():
    data = {
        'name': request.form['name'],
        'email': request.form['email'],
        'number': request.form['number'],
        'password': request.form['password'],
        'role': request.form.get('role', 'Normal user'),
        'balance': request.form.get('balance', 0.0),
    }
    create_user(data)
    return redirect(url_for('admin_bp.users_page'))


@admin_bp.route('/locations', methods=['POST'])
def create_location_admin():
    name = request.form['name']
    create_location({'name': name})
    return redirect(url_for('admin_bp.locations_page'))


@admin_bp.route('/rooms', methods=['POST'])
def create_room_admin():
    data = {
        'name': request.form['name'],
        'capacity': request.form['capacity'],
        'slot_price': request.form['slot_price'],
        'slot_duration': request.form['slot_duration'],
        'location_id': request.form['location_id'],
    }
    create_room(data)
    return redirect(url_for('admin_bp.rooms_page'))


@admin_bp.route('/rooms/delete/<int:room_id>', methods=['POST'])
def delete_room_admin(room_id):
    delete_room(room_id)
    return redirect(url_for('admin_bp.rooms_page'))


@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user_admin(user_id):
    delete_user(user_id)
    return redirect(url_for('admin_bp.users_page'))


@admin_bp.route('/users/<int:user_id>')
def user_detail(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return "User not found", 404
    balance = get_user_balance(user_id)
    recharges = get_user_recharges(user_id)
    return render_template('user_detail.html', user=user, balance=balance, recharges=recharges)


@admin_bp.route('/locations/<int:location_id>/rooms')
def location_rooms(location_id):
    from data_access1 import get_all_rooms, get_all_locations
    location = next((loc for loc in get_all_locations() if loc.id == location_id), None)
    if not location:
        return "Location not found", 404
    rooms = [room for room in get_all_rooms() if room.location_id == location_id]
    return render_template('location_rooms.html', location=location, rooms=rooms)


