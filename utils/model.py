import utils.database as db
import bcrypt

def find_user(username: str):
    # This now returns a single user object or None
    return db.get_user(username)

def add_user(username: str, password: str):
    return db.add_user(username, password)

def get_events(username: str):
    return db.get_entries(username)

def add_event(user_id, title, rating):
    db.create_event(user_id, title, rating)

def login(username: str, password: str):
    # get the user from the database
    user = db.get_user(username)
    
    print(f"Debug - login function user: {user}")
    
    if not user:
        print("Debug - No user found")
        return False
    
    # user is now a single object, not a list
    stored_password = user["password"]  # Remove [0] indexing
    print(f"Debug - stored password: {stored_password}")
    print(f"Debug - entered password: {password}")
    
    # check if the password is correct
    try:
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            print("Debug - Password match!")
            return True
        else:
            print("Debug - Password mismatch!")
            return False
    except Exception as e:
        print(f"Debug - Error checking password: {e}")
        return False