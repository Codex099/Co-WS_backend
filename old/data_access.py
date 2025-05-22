from old.fake_data import (users_db, locations_db, rooms_db, bookings_db, 
                             recharges_db, expenses_db, User, Location, Room, 
                             Booking, Recharge, Expense, generate_time_slots)


def get_all_users():
    return [user.to_dict() for user in users_db.values()]

def get_user_by_id(user_id):
    user = users_db.get(user_id)
    return user.to_dict() if user else None

def get_user_by_email(email):
    for user in users_db.values():
        if user.email == email:
            return user.to_dict()
    return None

def create_user(user_data):
    new_id = max([int(id) for id in users_db.keys()]) + 1 if users_db else 1  # pour id unique
    new_user = User(
        id=new_id,
        name=user_data.get('name', ''),
        email=user_data.get('email', ''),
        password=user_data.get('password', ''),
        role=user_data.get('role', 'guest'),
        balance=user_data.get('balance', 0.0)
    )
    users_db[new_id] = new_user
    return new_user.to_dict()

def update_user(user_id, user_data):
    user = users_db.get(user_id)
    if not user:
        return None
    for key, value in user_data.items():
        if hasattr(user, key):
            setattr(user, key, value)
    return user.to_dict()

def delete_user(user_id):
    if user_id in users_db:
        del users_db[user_id]
        return True
    return False
########################locatin###############################

def get_all_locations():
    return [location.to_dict() for location in locations_db.values()]

def get_location_by_id(location_id):
    location = locations_db.get(location_id)
    return location.to_dict() if location else None

def create_location(location_data):
    new_id = max([int(id) for id in locations_db.keys()]) + 1 if locations_db else 1
    new_location = Location(
        id=new_id,
        name=location_data.get('name', '')
    )
    locations_db[new_id] = new_location
    return new_location.to_dict()

def update_location(location_id, location_data):
    location = locations_db.get(location_id)
    if not location:
        return None
    if 'name' in location_data:
        location.name = location_data['name']
    return location.to_dict()

def delete_location(location_id):
    if location_id in locations_db:
        del locations_db[location_id]
        return True
    return 
########################## Romms ######################################

def get_all_rooms():
    return [room.to_dict() for room in rooms_db.values()]

def get_rooms_by_location(location_id):
    return [room.to_dict() for room in rooms_db.values() if room.location_id == location_id]

def get_room_by_id(room_id):
    room = rooms_db.get(room_id)
    return room.to_dict() if room else None

def create_room(room_data):
    new_id = max([int(id) for id in rooms_db.keys()]) + 1 if rooms_db else 1  
    new_room = Room(
        id=new_id,
        name=room_data.get('name', ''),
        location_id=room_data.get('location_id'),
        capacity=room_data.get('capacity', 0)
    )
    rooms_db[new_id] = new_room
    return new_room.to_dict()

def update_room(room_id, room_data):
    room = rooms_db.get(room_id)
    if not room:
        return None
    for key, value in room_data.items():
        if hasattr(room, key):
            setattr(room, key, value)
    return room.to_dict()

def delete_room(room_id):
    if room_id in rooms_db:
        del rooms_db[room_id]
        return True
    return False
############################ boolings ####################################

def get_all_bookings():
    return [booking.to_dict() for booking in bookings_db.values()]

def get_booking_by_id(booking_id):
    booking = bookings_db.get(booking_id)
    return booking.to_dict() if booking else None

def get_user_bookings(user_id):
    return [booking.to_dict() for booking in bookings_db.values() if booking.user_id == user_id]

def get_room_bookings(room_id):
    return [booking.to_dict() for booking in bookings_db.values() if booking.room_id == room_id]

def create_booking(booking_data):
    user_id = booking_data.get('user_id')
    room_id = booking_data.get('room_id')
    date = booking_data.get('date')
    time_slots = booking_data.get('time_slots', [])  # Expecting a list of slots

    created_bookings = []
    new_id = max([int(id) for id in bookings_db.keys()]) + 1 if bookings_db else 1

    for slot in time_slots:
        # Check if the slot is already booked
        if not check_room_availability(room_id, date, slot):
            continue  # Skip already booked slots
        new_booking = Booking(
            id=new_id,
            user_id=user_id,
            room_id=room_id,
            date=date,
            time_slot=slot
        )
        bookings_db[new_id] = new_booking
        created_bookings.append(new_booking.to_dict())
        new_id += 1

    return created_bookings  # List of created bookings

def update_booking(booking_id, booking_data):
    booking = bookings_db.get(booking_id)
    if not booking:
        return None
    for key, value in booking_data.items():
        if hasattr(booking, key):
            setattr(booking, key, value)
    return booking.to_dict()

def delete_booking(booking_id):
    if booking_id in bookings_db:
        del bookings_db[booking_id]
        return True
    return False

def check_room_availability(room_id, date, time_slot):
    for booking in bookings_db.values():
        if (booking.room_id == room_id and 
            booking.date == date and 
            booking.time_slot == time_slot):
            return False
    return True

def search_available_rooms(date, time_slot, location_id=None, capacity=None):
    booked_room_ids = []
    for booking in bookings_db.values():
        if booking.date == date and booking.time_slot == time_slot:
            booked_room_ids.append(booking.room_id)
    available_rooms = []
    for room in rooms_db.values():
        if room.id in booked_room_ids:
            continue
        available_rooms.append(room.to_dict())
    return available_rooms
################################################################

def get_user_recharges(user_id):
    return [recharge.to_dict() for recharge in recharges_db.values() if recharge.user_id == user_id]

def get_user_expenses(user_id):
    return [expense.to_dict() for expense in expenses_db.values() if expense.user_id == user_id]

def create_recharge(recharge_data):
    user_id = recharge_data.get('user_id')
    amount = recharge_data.get('amount', 0.0)
    user = users_db.get(user_id)
    if not user:
        return None
    new_id = max([int(id) for id in recharges_db.keys()]) + 1 if recharges_db else 1
    new_recharge = Recharge(
        id=new_id,
        user_id=user_id,
        amount=amount,
        date=recharge_data.get('date')
    )
    recharges_db[new_id] = new_recharge
    user.balance += amount
    return new_recharge.to_dict()

def create_expense(expense_data):
    user_id = expense_data.get('user_id')
    amount = expense_data.get('amount', 0.0)
    user = users_db.get(user_id)
    if not user:
        return None
    if user.balance < amount:
        return None
    new_id = max([int(id) for id in expenses_db.keys()]) + 1 if expenses_db else 1
    new_expense = Expense(
        id=new_id,
        user_id=user_id,
        amount=amount,
        booking_id=expense_data.get('booking_id'),
        date=expense_data.get('date')
    )
    expenses_db[new_id] = new_expense
    user.balance -= amount
    return new_expense.to_dict()

def get_user_balance(user_id):
    user = users_db.get(user_id)
    return user.balance if user else None

def get_available_slots(room_id, date):
    all_slots = generate_time_slots()
    booked_slots = [
        booking.time_slot
        for booking in bookings_db.values()
        if booking.room_id == room_id and booking.date == date
    ]
    return [slot for slot in all_slots if slot not in booked_slots]