import data_access1
import random
from datetime import datetime, timedelta, time

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
    user = data_access1.create_user(data)
    return {"message": "User created", "user_id": user.id}, 201

def list_users():
    users = data_access1.get_all_users()
    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "number": user.number,  
            "role": user.role,
            "balance": user.balance
        }
        for user in users
    ]

def get_user_by_email(email):
    user = data_access1.get_user_by_email(email)
    if not user:
        return {"error": "User not found"}, 404
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "balance": user.balance
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
    if not data or not all(k in data for k in ("user_id", "room_id", "date", "start_time", "slot_count")):
        return {"error": "Missing data"}, 400

    # Récupérer la salle
    room = next((r for r in data_access1.get_all_rooms() if r.id == data['room_id']), None)
    if not room:
        return {"error": "Room not found"}, 404

    slot_duration = room.slot_duration            # minutes
    booking_start = datetime.strptime(f"{data['date']} {data['start_time']}", "%Y-%m-%d %H:%M")
    booking_end = booking_start + timedelta(minutes=slot_duration * data['slot_count'])

    # Vérifier la disponibilité
    for booking in data_access1.get_all_bookings():
        if booking.room_id == data['room_id'] and str(booking.date) == data['date']:
            existing_start = datetime.combine(booking.date, booking.start_time)
            existing_end = existing_start + timedelta(minutes=slot_duration * booking.slot_count)
            if not (booking_end <= existing_start or booking_start >= existing_end):
                return {"error": "Room not available for this time slot"}, 409

    # Calcul du prix total
    slot_price = room.slot_price 
    total_price = slot_price * data['slot_count']

    # Créer la réservation
    booking_data = {
        "user_id": data['user_id'],
        "room_id": data['room_id'],
        "date": data['date'],
        "start_time": data['start_time'],
        "slot_count": data['slot_count'],
        "total_price": total_price
    }
    booking = data_access1.create_booking(booking_data)

    # Décrémenter le balance de l'utilisateur
    user = data_access1.get_user_by_id(data['user_id'])
    if user.balance < total_price:
        # Annuler la réservation si le solde est insuffisant
        data_access1.delete_booking(booking.id)
        return {"error": "Insufficient balance"}, 400

    user.balance -= total_price
    data_access1.save_user(user)  # save change pour l'utilisateur

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

