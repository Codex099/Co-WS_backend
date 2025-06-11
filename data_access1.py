from models import db, User, Location, Room, Booking, Recharge
from datetime import datetime

# --- User ---
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

def get_user_by_number(number):
    return User.query.filter_by(number=number).first()

def create_user(data):
    user = User(
        name=data['name'],
        email=data['email'],
        number=data['number'],
        password=data['password'],
        role=data.get('role', 'user'),
        balance=data.get('balance', 0.0)
    )
    db.session.add(user)
    db.session.commit()
    return user

def get_user_balance(user_id):
    user = User.query.get(user_id)
    if not user:
        return 0.0
    return user.balance

def get_user_by_id(user_id):
    return User.query.get(user_id)

def save_user(user):
    db.session.commit()

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True

def get_all_users():
    return User.query.all()

# --- Recharge ---
def create_recharge(data):
    user = get_user_by_id(data['user_id'])
    if not user:
        return None
    recharge = Recharge(user_id=user.id, amount=data['amount'], date=datetime.utcnow())
    db.session.add(recharge)
    user.balance += data['amount']
    db.session.add(user)
    db.session.commit()
    return recharge

def get_user_recharges(user_id):
    return Recharge.query.filter_by(user_id=user_id).order_by(Recharge.date.desc()).all()

# --- Location ---
def create_location(data):
    image_data = data.get('image_data')
    location = Location(
        name=data['name'],
        image_data=image_data
    )
    db.session.add(location)
    db.session.commit()
    return location

def get_all_locations():
    return Location.query.all()

# --- Room ---
def create_room(data):
    room = Room(
        name=data['name'],
        capacity=data['capacity'],
        slot_price=data['slot_price'],
        slot_duration=data['slot_duration'],
        location_id=data['location_id'],
        image_data=data.get('image_data')
    )
    db.session.add(room)
    db.session.commit()
    return room

def get_all_rooms():
    return Room.query.all()

def update_room(room_id, data):
    room = Room.query.get(room_id)
    if not room:
        return None
    room.name = data.get('name', room.name)
    room.capacity = data.get('capacity', room.capacity)
    room.hourly_price = data.get('hourly_price', room.hourly_price)
    room.location_id = data.get('location_id', room.location_id)
    room.slot_price = data.get('slot_price', room.slot_price)
    db.session.commit()
    return room

def delete_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return False
    db.session.delete(room)
    db.session.commit()
    return True

# --- Booking ---
def create_booking(data):
    if isinstance(data['date'], str):
        date_obj = datetime.strptime(data['date'], "%Y-%m-%d").date()
    else:
        date_obj = data['date']
    if isinstance(data['start_time'], str):
        time_obj = datetime.strptime(data['start_time'], "%H:%M").time()
    else:
        time_obj = data['start_time']

    booking = Booking(
        user_id=data['user_id'],
        room_id=data['room_id'],
        date=date_obj,
        start_time=time_obj,
        slot_count=data['slot_count'],
        total_price=data.get('total_price')
    )
    db.session.add(booking)
    db.session.commit()
    return booking

def get_all_bookings():
    return Booking.query.all()

def update_booking(booking_id, data):
    booking = Booking.query.get(booking_id)
    if not booking:
        return None
    booking.user_id = data.get('user_id', booking.user_id)
    booking.room_id = data.get('room_id', booking.room_id)
    booking.date = data.get('date', booking.date)
    booking.start_time = data.get('start_time', booking.start_time)
    booking.end_time = data.get('end_time', booking.end_time)
    booking.total_price = data.get('total_price', booking.total_price)
    db.session.commit()
    return booking

def delete_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if not booking:
        return False
    db.session.delete(booking)
    db.session.commit()
    return True

# --- Recharge ---
def create_recharge(data):
    user = get_user_by_id(data['user_id'])
    if not user:
        return None
    recharge = Recharge(user_id=user.id, amount=data['amount'], date=datetime.utcnow())
    db.session.add(recharge)
    user.balance += data['amount']
    db.session.add(user)
    db.session.commit()
    return recharge

def get_all_recharges():
    return Recharge.query.all()

def update_recharge(recharge_id, data):
    recharge = Recharge.query.get(recharge_id)
    if not recharge:
        return None
    recharge.user_id = data.get('user_id', recharge.user_id)
    recharge.amount = data.get('amount', recharge.amount)
    recharge.date = data.get('date', recharge.date)
    db.session.commit()
    return recharge

def delete_recharge(recharge_id):
    recharge = Recharge.query.get(recharge_id)
    if not recharge:
        return False
    db.session.delete(recharge)
    db.session.commit()
    return True