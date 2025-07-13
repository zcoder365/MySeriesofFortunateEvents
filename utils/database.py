from pymongo import MongoClient
import os
from dotenv import load_dotenv
import bcrypt
from datetime import datetime

# load the environment variables from the .env file
load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DBNAME = os.getenv("MONGODB_DBNAME")

if not MONGODB_URI or not MONGODB_DBNAME:
    print("ERROR: MongoDB environment variables not found!")
    print("Make sure you have a .env file with MONGODB_URI and MONGODB_DBNAME")
    exit(1)

try:
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DBNAME]
    users_col = db["users"]
    entries_col = db["entries"]
    print("Debug - MongoDB client created successfully")
except Exception as e:
    print(f"ERROR creating MongoDB client: {e}")
    exit(1)

# USER FUNCTIONS
# add a user to the database
def add_user(username: str, password: str):
    try:
        # Hash the password before storing
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # create a user entry
        new_user_entry = {
            "username": username,
            "password": hashed_password.decode('utf-8'),  # Store as string
            "entry_count": 0,
            "num_entries": 0,
            "streak": 0
        }
        
        # add a user to the database
        result = users_col.insert_one(new_user_entry)
        print(f"Debug - add_user inserted_id: {result.inserted_id}")
        return str(result.inserted_id)
        
    except Exception as e:
        print(f"Error adding user: {e}")
        return None

# get a user from the database
def get_user(username: str):
    try:
        # Execute the query - errors will be raised as exceptions
        user = users_col.find_one({"username": username})
        
        # Debug: Print what we got back
        print(f"Debug - get_user result: {user}")
        
        return user  # Return single user object
            
    except Exception as e:
        # Handle any database errors that occur
        print(f"Error getting user: {e}")
        return None

# ENTRY FUNCTIONS
# add an entry to the database
def add_entry(entry: str, rating: int, username: str): 
    try:
        # create an entry
        new_entry = {
            "entry": entry,
            "rating": rating,
            "username": username,
            "created_at": datetime.today().strftime('%Y-%m-%d %H:%M:%S') # Store as string
        }
        
        # add an entry to the database
        result = entries_col.insert_one(new_entry)
        # increment entry_count and num_entries for the user
        users_col.update_one(
            {"username": username},
            {"$inc": {"entry_count": 1, "num_entries": 1}}
        )
        print(f"Debug - add_entry inserted_id: {result.inserted_id}")
        return str(result.inserted_id)
        
    except Exception as e:
        print(f"Error adding entry: {e}")
        return None

def get_entries(username: str):
    try:
        # get all entries from the database
        entries = list(entries_col.find({"username": username}))
        
        return entries
        
    except Exception as e:
        print(f"Error getting entries: {e}")
        return []

def get_entries_by_date(username: str, date: str):
    try:
        # get all entries from the database
        entries = list(entries_col.find({"username": username, "created_at": date}))
        
        return entries
        
    except Exception as e:
        print(f"Error getting entries by date: {e}")
        return []

def get_user_streak(username: str):
    try:
        # get the user streak from the database
        user = users_col.find_one({"username": username}, {"streak": 1})
        return user.get("streak", 0) if user else 0
        
    except Exception as e:
        print(f"Error getting user streak: {e}")
        return 0

def update_user_streak(username: str, streak: int):
    try:
        # update the user streak in the database
        result = users_col.update_one({"username": username}, {"$set": {"streak": streak}})
        print(f"Debug - update_user_streak matched: {result.matched_count}, modified: {result.modified_count}")
        return result.modified_count > 0
        
    except Exception as e:
        print(f"Error updating user streak: {e}")
        return None

def increment_user_entries_count(username: str):
    try:
        # Get current count
        user = users_col.find_one({"username": username}, {"num_entries": 1})
        
        if not user:
            print(f"User {username} not found")
            return False
        
        old_count = user.get("num_entries", 0)
        new_count = old_count + 1
        
        print(f"Updating {username} from {old_count} to {new_count}")
        
        # Do the update (don't worry about the response)
        result = users_col.update_one({"username": username}, {"$set": {"num_entries": new_count}})
        
        # Check if it actually changed
        after = users_col.find_one({"username": username}, {"num_entries": 1})
        actual_count = after.get("num_entries", 0)
        
        if actual_count == new_count:
            print(f"✅ Success! Count is now {actual_count}")
            return True
        
        else:
            print(f"❌ Failed! Count is still {actual_count}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False