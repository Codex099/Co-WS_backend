from models import db, User

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
    return User.query.all()