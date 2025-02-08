import utils.database as db

def find_user(username):
    return db.get_user(username)

def find_events(user_id):
    return db.get_events(user_id)