import utils.database as db

def create_database():
    db.create_db()

def find_user(username):
    return db.get_user(username)

def check_password(password, hashed_password):
    return db.check_password(password, hashed_password)

def add_user(username, password):
    db.create_user(username, password)

def find_events(user_id):
    return db.get_events(user_id)

def can_add_entry(user_id):
    return db.get_event_by_date(user_id)

def add_event(user_id, title, rating):
    db.create_event(user_id, title, rating)
    
def hash_password(password):
    return db.hash_password(password)