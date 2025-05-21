from app.firebase_config import db
from werkzeug.security import generate_password_hash, check_password_hash

def add_user(username, password):
    user_ref = db.collection("users").document(username)
    user_ref.set({
        "username": username,
        "password": generate_password_hash(password)
    })

def get_user(username):
    user_doc = db.collection("users").document(username).get()
    if user_doc.exists:
        return user_doc.to_dict()
    return None

def validate_user(username, password):
    user = get_user(username)
    if user and check_password_hash(user["password"], password):
        return True
    return False
