from datetime import datetime, timedelta
import random
import json

class User:
    def __init__(self, id, name, email, password, role='guest', balance=0.0):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.balance = balance
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'balance': self.balance
        }

class Location:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Room:
    def __init__(self, id, name, location_id, capacity):
        self.id = id
        self.name = name
        self.location_id = location_id
        self.capacity = capacity
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location_id': self.location_id,
            'capacity': self.capacity
        }

class Booking:
    def __init__(self, id, user_id, room_id, date, time_slot):
        self.id = id
        self.user_id = user_id
        self.room_id = room_id
        self.date = date
        self.time_slot = time_slot
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'room_id': self.room_id,
            'date': self.date,
            'time_slot': self.time_slot
        }

class Recharge:
    def __init__(self, id, user_id, amount, date=None):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'date': self.date
        }

class Expense:
    def __init__(self, id, user_id, amount, booking_id, date=None):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.booking_id = booking_id
        self.date = date if date else datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'booking_id': self.booking_id,
            'date': self.date
        }

# Dictionnaires pour stocker les données
users_db = {}
locations_db = {}
rooms_db = {}
bookings_db = {}
recharges_db = {}
expenses_db = {}

def init_DB():
    #Initialiser la base de données 
    users = [
        User(1, "Admin", "admin@cowork.com", "admin123", "admin", 1000.0),
        User(2, "Ahmed", "ahmed@example.com", "password123", "user", 500.0),
        User(3, "Sara", "sara@example.com", "password123", "user", 300.0),
        User(4, "Khaled", "mohamed@example.com", "password123", "user", 150.0),
        User(5, "Akram", "fatima@example.com", "password123", "guest", 0.0),
        User(6, "Hafid", "omar@example.com", "password123", "guest", 0.0),
    ]
    locations = [
        Location(1, "Maravale"),
        Location(2, "Es_senai"),
        Location(3, "Usto"),
    ]
    rooms = [
        # emplacement id 1
        Room(1, "Salle de formation", 1, 15),  
        Room(2, "Salle de réunion", 1, 10),
        Room(3, "Salle de bureau", 1, 20),
        Room(4, "Salle de conférence ", 1, 25),
        Room(5, "Salle de téléconférence ", 2, 8),
        Room(6, "Bureau individuel ", 2, 1),
        # emplacement id 2
        Room(7, "Salle de formation", 2, 20),  
        Room(8, "Salle de réunion", 2, 12),
        Room(9, "Salle de bureau", 2, 27),
        Room(10, "Salle de conférence ", 2, 25),
        Room(11, "Salle de téléconférence ", 2, 12),
        Room(12, "Bureau individuel ", 2, 1),
        # emplacement id 3
        Room(13, "Salle de formation", 3, 22),  
        Room(14, "Salle de réunion", 3, 10),
        Room(15, "Salle de bureau", 3, 22),
        Room(16, "Salle de conférence ", 3, 23),
        Room(17, "Salle de téléconférence ", 3, 12),
        Room(18, "Bureau individuel ", 3, 1),
    ]
    bookings = []
    booking_id = 1
    time_slots = [f"{str(h).zfill(2)}:00-{str((h+1)%24).zfill(2)}:00" for h in range(24)]
    
    today = datetime.now()
    user_ids = [2, 3, 4]
    for i in range(20):
        user_id = random.choice(user_ids)
        room_id = random.randint(1, 10)
        days_offset = random.randint(0, 14)
        booking_date = (today + timedelta(days=days_offset)).strftime("%Y-%m-%d")
        time_slot = random.choice(time_slots)
        bookings.append(Booking(booking_id, user_id, room_id, booking_date, time_slot))
        booking_id += 1

    recharges = [
        Recharge(1, 2, 200.0, (today - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")),
        Recharge(2, 2, 300.0, (today - timedelta(days=5)).strftime("%Y-%m-%d %H:%M:%S")),
        Recharge(3, 3, 300.0, (today - timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")),
        Recharge(4, 4, 150.0, (today - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")),
    ]
    expenses = [
        Expense(1, 2, 50.0, 1, (today - timedelta(days=8)).strftime("%Y-%m-%d %H:%M:%S")),
        Expense(2, 2, 25.0, 3, (today - timedelta(days=6)).strftime("%Y-%m-%d %H:%M:%S")),
        Expense(3, 3, 100.0, 5, (today - timedelta(days=4)).strftime("%Y-%m-%d %H:%M:%S")),
        Expense(4, 4, 75.0, 7, (today - timedelta(days=2)).strftime("%Y-%m-%d %H:%M:%S")),
    ]
    users_dict = {user.id: user for user in users}
    locations_dict = {location.id: location for location in locations}
    rooms_dict = {room.id: room for room in rooms}
    bookings_dict = {booking.id: booking for booking in bookings}
    recharges_dict = {recharge.id: recharge for recharge in recharges}
    expenses_dict = {expense.id: expense for expense in expenses}
    return users_dict, locations_dict, rooms_dict, bookings_dict, recharges_dict, expenses_dict

users_db, locations_db, rooms_db, bookings_db, recharges_db, expenses_db = init_DB()

def save_to_json():
                       #save as JSON
    data = {
        'users': {str(k): v.to_dict() for k, v in users_db.items()},
        'locations': {str(k): v.to_dict() for k, v in locations_db.items()},
        'rooms': {str(k): v.to_dict() for k, v in rooms_db.items()},
        'bookings': {str(k): v.to_dict() for k, v in bookings_db.items()},
        'recharges': {str(k): v.to_dict() for k, v in recharges_db.items()},
        'expenses': {str(k): v.to_dict() for k, v in expenses_db.items()},
    }
    with open('cowork_fake_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("Les données fictives ont été enregistrées dans le fichier 'cowork_fake_data.json'")

if __name__ == "__main__":
    save_to_json()