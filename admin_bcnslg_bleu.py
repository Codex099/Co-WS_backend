from flask import Blueprint, render_template, request, redirect, url_for, session
from data_access1 import (
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
    get_all_users,  
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
    image_file = request.files.get('image')
    image_data = None
    if image_file:
        image_data = image_file.read()
    create_location({'name': name, 'image_data': image_data})
    return redirect(url_for('admin_bp.locations_page'))


@admin_bp.route('/rooms', methods=['POST'])
def create_room_admin():
    name = request.form['name']
    capacity = request.form['capacity']
    slot_price = request.form['slot_price']
    slot_duration = request.form['slot_duration']
    location_id = request.form['location_id']
    image = request.files.get('image')
    image_data = image.read() if image else None

    create_room({
        'name': name,
        'capacity': capacity,
        'slot_price': slot_price,
        'slot_duration': slot_duration,
        'location_id': location_id,
        'image_data': image_data
    })
    return redirect(url_for('admin_bp.rooms_page'))


@admin_bp.route('/rooms/delete/<int:room_id>', methods=['POST'])
def delete_room_admin(room_id):
    delete_room(room_id)
    return redirect(url_for('admin_bp.rooms_page'))


@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
def delete_user_admin(user_id):
    delete_user(user_id)
    return redirect(url_for('admin_bp.users_page'))


@admin_bp.route('/locations/delete/<int:location_id>', methods=['POST'])
def delete_location_admin(location_id):
    from data_access1 import delete_location
    delete_location(location_id)
    return redirect(url_for('admin_bp.locations_page'))


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


@admin_bp.route('/bookings')
def bookings_page():
    from data_access1 import get_all_bookings
    search_email = request.args.get('search_email', '').strip().lower()
    bookings = get_all_bookings()
    if search_email:
        bookings = [b for b in bookings if b.user and b.user.email and search_email in b.user.email.lower()]
    return render_template('bookings.html', bookings=bookings)





