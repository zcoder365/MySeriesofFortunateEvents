import utils.database as db

def find_user(username):
    return db.get_user(username)

def check_password(password, hashed_password):
    return db.check_password(password, hashed_password)

def add_user(username, password):
    db.create_user(username, password)

def find_events(user_id):
    return db.get_events(user_id)