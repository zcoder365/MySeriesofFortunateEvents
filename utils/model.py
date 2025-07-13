import utils.database as db
import bcrypt

def find_user(username: str):
    # Returns a single user object or None
    return db.get_user(username)

def add_user(username: str, password: str):
    return db.add_user(username, password)

def get_events(username: str):
    return db.get_entries(username)

def login(username: str, password: str):
    # get the user from the database
    user = db.get_user(username)
    
    print(f"Debug - login function user: {user}")
    
    if not user:
        print("Debug - No user found")
        return False
    
    stored_password = user["password"]
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

def update_streak(username: str):
    # get the user's current streak from the database
    user_current_streak = db.get_user_streak(username)
    
    # increment the user's streak by 1
    new_streak = user_current_streak + 1
    
    # update the user's streak in the database
    db.update_user_streak(username, new_streak)