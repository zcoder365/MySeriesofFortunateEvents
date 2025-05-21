import utils.database as db
import bcrypt

def find_user(username: str):
    return db.get_user(username)

def add_user(username: str, password: str):
    return db.add_user(username, password)

def get_events(username: str):
    return db.get_entries(username)

def add_event(user_id, title, rating):
    db.create_event(user_id, title, rating)