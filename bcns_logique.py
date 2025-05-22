import data_access1

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
            "number": user.number,  # Ajout ici
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