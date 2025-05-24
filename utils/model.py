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
    return db.add_entry(user_id, title, rating)

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

def update_streak(username: str):
    # get the user's current streak from the database
    user_current_streak = db.get_user_streak(username)
    
    # increment the user's streak by 1
    new_streak = user_current_streak + 1
    
    # update the user's streak in the database
    db.update_user_streak(username, new_streak)

def update_user_entries_count(username: str):
    # get the user's current entry count from the database
    user_current_entry_count = db.get_user_entries_count(username)
    
    # increment the user's entry count by 1
    new_entry_count = user_current_entry_count + 1
    
    # update the user's entry count in the database
    db.update_user_entries_count(username, new_entry_count)