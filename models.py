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
    bookings = db.relationship('Booking', backref='user', lazy=True)
    recharges = db.relationship('Recharge', backref='user', lazy=True)
    expenses = db.relationship('Expense', backref='user', lazy=True)

class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rooms = db.relationship('Room', backref='location', lazy=True)

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    hourly_price = db.Column(db.Float, nullable=True)  
    location_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=False)
    bookings = db.relationship('Booking', backref='room', lazy=True)

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)  
    start_time = db.Column(db.Time, nullable=False)  
    end_time = db.Column(db.Time, nullable=False)    
    total_price = db.Column(db.Float, nullable=True) 

class Recharge(db.Model):   #ychof + ymodifier
    __tablename__ = 'recharges'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)