from models import db, User, Location, Room, Booking, Recharge

#user
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

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

def get_all_users():
    users = User.query.all()
    result = []
    for user in users:
        balance = get_user_balance(user.id)
        result.append({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'number': user.number,
            'role': user.role,
            'balance': balance
        })
    return result

def update_user(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return None
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.number = data.get('number', user.number)
    user.password = data.get('password', user.password)
    user.role = data.get('role', user.role)
    db.session.commit()
    return user

def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return False
    db.session.delete(user)
    db.session.commit()
    return True

def get_user_balance(user_id):
    user = User.query.get(user_id)
    if not user:
        return 0.0
    total_recharge = db.session.query(db.func.sum(Recharge.amount)).filter_by(user_id=user_id).scalar() or 0.0
    return user.balance + total_recharge

def get_user_by_id(user_id):
    return User.query.get(user_id)

def create_recharge(data):
    recharge = Recharge(
        user_id=data['user_id'],
        amount=data['amount']
    )
    db.session.add(recharge)
    db.session.commit()
    return recharge

def save_user(user):
    db.session.commit()

def get_user_by_number(number):
    return User.query.filter_by(number=number).first()

#loaction
def create_location(data):
    image_data = data.get('image_data')  #  binaire
    location = Location(
        name=data['name'],
        image_data=image_data
    )
    db.session.add(location)
    db.session.commit()
    return location

def get_all_locations():
    return Location.query.all()

def update_location(location_id, data):
    location = Location.query.get(location_id)
    if not location:
        return None
    location.name = data.get('name', location.name)
    db.session.commit()
    return location

def delete_location(location_id):
    location = Location.query.get(location_id)
    if not location:
        return False
    db.session.delete(location)
    db.session.commit()
    return True

#Room
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

#Booking 
def create_booking(data):
    booking = Booking(
        user_id=data['user_id'],
        room_id=data['room_id'],
        date=data['date'],
        start_time=data['start_time'],
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

#Recharge
def create_recharge(data):
    recharge = Recharge(
        user_id=data['user_id'],
        amount=data['amount'],
        date=data.get('date')
    )
    db.session.add(recharge)
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

def get_user_recharges(user_id):
    return Recharge.query.filter_by(user_id=user_id).order_by(Recharge.date.desc()).all()