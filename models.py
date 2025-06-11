from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    number = db.Column(db.Integer,unique=True,nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), default='Normal user')
    balance = db.Column(db.Float, default=0.0)
    bookings = db.relationship('Booking', backref='user') 
    recharges = db.relationship('Recharge', backref='user')

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=True) #largebinary -----> pour image
    rooms = db.relationship('Room', backref='location')

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    slot_price = db.Column(db.Float, nullable=False)  
    slot_duration =db.Column(db.Integer,nullable=False,default=60)  #ppar défault 1h
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    bookings = db.relationship('Booking', backref='room')
    image_data = db.Column(db.LargeBinary)  

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)  
    start_time = db.Column(db.Time, nullable=False)
    slot_count = db.Column(db.Integer, nullable=False)    # nombre de slot réservé
    total_price = db.Column(db.Float, nullable=True) 

class Recharge(db.Model):   #ychof + ymodifier
    __tablename__ = 'recharges'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)