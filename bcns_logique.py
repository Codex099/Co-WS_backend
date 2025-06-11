import data_access1
import random
from datetime import datetime, timedelta, time
import base64

# Pour stocker temporairement les codes et les données d'inscription
signup_codes = {}
pending_users = {}

def create_user(data):
    if not data or not all(k in data for k in ("name", "email", "password", "number",)):
        return {"error": "Missing data"}, 400
    if not data['email'] or not data['number']:
        return {"error": "Email or number cannot be null"}, 400
    if data_access1.get_user_by_email(data['email']):
        return {"error": "Email already exists"}, 400
    # Vérifie aussi le numéro
    if data_access1.get_user_by_number(data['number']):
        return {"error": "Number already exists"}, 400
    user = data_access1.create_user(data)
    return {"message": "User created", "user_id": user.id}, 201



def get_user_by_email(email):
    user = data_access1.get_user_by_email(email)
    if not user:
        return {"error": "User not found"}, 404
    balance = data_access1.get_user_balance(user.id)
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "balance": balance,
        "number": user.number   # <-- ce champ doit être présent ici
    }, 200

def login_user(data):
    if not data or not all(k in data for k in ("email", "password")):
        return {"error": "Missing data"}, 400
    user = data_access1.get_user_by_email(data['email'])
    if not user or user.password != data['password']:
        return {"error": "Invalid credentials"}, 401
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "balance": user.balance
    }, 200

def signup_request(data):
    if not data or not all(k in data for k in ("name", "email", "password", "number")):
        return {"error": "Missing data"}, 400
    if not data['email'] or not data['number']:
        return {"error": "Email or number cannot be null"}, 400
    if data_access1.get_user_by_email(data['email']):
        return {"error": "Email already exists"}, 400

    code = str(random.randint(10000, 99999))
    signup_codes[data['email']] = code
    pending_users[data['email']] = data  ## pour stock les info 

    print(f"Code de confirmation pour {data['email']} : {code}")  

    return {"message": "Confirmation code sent (see terminal)", "email": data['email']}, 200

def confirm_signup(email, code):
    expected_code = signup_codes.get(email)
    if not expected_code:
        return {"error": "No code found for this email"}, 400
    if code != expected_code:
        return {"error": "Invalid code"}, 401

    # Créer l'utilisateur
    
    user = data_access1.create_user(pending_users[email])

    # Nettoyer
    del signup_codes[email]
    del pending_users[email]

    return {"message": "User created", "user_id": user.id}, 201



def create_booking(data):
    user = data_access1.get_user_by_id(data['user_id'])
    room = next((r for r in data_access1.get_all_rooms() if r.id == data['room_id']), None)
    if not user or not room:
        return {"error": "User or room not found"}, 404

    slot_price = room.slot_price
    total_price = slot_price * data['slot_count']

    if user.balance < total_price:
        return {"error": "Insufficient balance"}, 400

    # Décrémente le solde
    user.balance -= total_price
    data_access1.save_user(user)

    booking = data_access1.create_booking({
        "user_id": data['user_id'],
        "room_id": data['room_id'],
        "date": data['date'],
        "start_time": data['start_time'],
        "slot_count": data['slot_count'],
        "total_price": total_price
    })
    return {"message": "Booking created", "booking_id": booking.id}, 201

def get_available_slots_range(room_id, start_date_str, end_date_str):
    room = next((r for r in data_access1.get_all_rooms() if r.id == room_id), None)
    if not room:
        return {"error": "Room not found"}, 404

    slot_duration = room.slot_duration
    opening_time = time(8, 0)
    closing_time = time(20, 0)

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    result = {}

    for n in range((end_date - start_date).days + 1):
        current_date = start_date + timedelta(days=n)
        slots = []
        current = datetime.combine(current_date, opening_time)
        closing = datetime.combine(current_date, closing_time)
        while current + timedelta(minutes=slot_duration) <= closing:
            slots.append(current.time().strftime('%H:%M'))
            current += timedelta(minutes=slot_duration)

        bookings = [
            b for b in data_access1.get_all_bookings()
            if b.room_id == room_id and str(b.date) == str(current_date)
        ]

        unavailable = set()
        for booking in bookings:
            booking_start = datetime.combine(booking.date, booking.start_time)
            for i in range(booking.slot_count):
                slot_time = (booking_start + timedelta(minutes=i * slot_duration)).time().strftime('%H:%M')
                unavailable.add(slot_time)

        available_slots = [slot for slot in slots if slot not in unavailable]
        result[str(current_date)] = {
            "available_slots": available_slots,
            "unavailable_slots": list(unavailable)
        }

    return result, 200

def create_recharge(data):
    user = data_access1.get_user_by_id(data['user_id'])
    if not user:
        return {"error": "User not found"}, 404

    # Créer la recharge
    recharge = data_access1.create_recharge(data)

    # Mettre à jour le balance
    user.balance += data['amount']
    data_access1.save_user(user)

    return {"message": "Recharge successful", "new_balance": user.balance}, 201

def get_all_locations():
    locations = data_access1.get_all_locations()
    result = []
    for loc in locations:
        image_base64 = None
        if loc.image_data:
            image_base64 = base64.b64encode(loc.image_data).decode('utf-8')
        result.append({
            "id": loc.id,
            "name": loc.name,
            "image_base64": image_base64
        })
    return result, 200

def get_rooms_by_location_name(location_name):
    # Trouver la location par nom
    location = next((loc for loc in data_access1.get_all_locations() if loc.name == location_name), None)
    if not location:
        return {"error": "Location not found"}, 404

    # Récupérer les rooms de cette location
    rooms = [room for room in data_access1.get_all_rooms() if room.location_id == location.id]
    result = []
    for room in rooms:
        image_base64 = None
        if getattr(room, "image_data", None):
            import base64
            image_base64 = base64.b64encode(room.image_data).decode('utf-8')
        result.append({
            "id": room.id,
            "name": room.name,
            "capacity": room.capacity,
            "slot_price": room.slot_price,
            "slot_duration": room.slot_duration,
            "image_base64": image_base64
        })
    return result, 200

def get_user_by_id(user_id):
    user = data_access1.get_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}, 404
    balance = data_access1.get_user_balance(user.id)
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "balance": balance,
        "number": user.number
    }, 200

def update_user_by_id(user_id, data):
    user = data_access1.get_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}, 404
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.number = data.get('number', user.number)
    data_access1.save_user(user)
    return {"message": "User updated"}, 200

def get_user_reservations(user_id):
    bookings = [b for b in data_access1.get_all_bookings() if b.user_id == user_id]
    result = []
    for b in bookings:
        room = data_access1.get_all_rooms()
        room = next((r for r in room if r.id == b.room_id), None)
        location = data_access1.get_all_locations()
        location = next((l for l in location if l.id == room.location_id), None) if room else None
        image_base64 = None
        if getattr(room, "image_data", None):
            import base64
            image_base64 = base64.b64encode(room.image_data).decode('utf-8')
        result.append({
            "room_name": room.name if room else "",
            "location": location.name if location else "",
            "date": b.date.strftime("%Y-%m-%d"),
            "start_time": b.start_time.strftime("%H:%M"),
            "slot_count": b.slot_count,
            "price": b.total_price,
            "room_image": f"data:image/jpeg;base64,{image_base64}" if image_base64 else "",
            "status": "Confirmed"
        })
    return result, 200

