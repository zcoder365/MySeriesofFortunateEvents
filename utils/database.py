from supabase import create_client, Client
import os
from dotenv import load_dotenv
import bcrypt
from datetime import datetime

# load the environment variables from the .env file
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# Debug: Print environment variables (be careful with this in production!)
print(f"Debug - SUPABASE_URL: {SUPABASE_URL}")
print(f"Debug - SUPABASE_KEY: {SUPABASE_KEY[:20]}..." if SUPABASE_KEY else "Debug - SUPABASE_KEY: None")

# Check if environment variables are loaded
if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: Supabase environment variables not found!")
    print("Make sure you have a .env file with SUPABASE_URL and SUPABASE_ANON_KEY")
    exit(1)

try:
    # create a client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    print("Debug - Supabase client created successfully")
except Exception as e:
    print(f"ERROR creating Supabase client: {e}")
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
            "password": hashed_password.decode('utf-8')  # Store as string
        }
        
        # add a user to the database
        response = supabase.table("users").insert(new_user_entry).execute()
        
        print(f"Debug - add_user response: {response.data}")
        return response.data
        
    except Exception as e:
        print(f"Error adding user: {e}")
        return None

# get a user from the database
def get_user(username: str):
    try:
        # Execute the query - errors will be raised as exceptions
        response = supabase.table("users").select("*").eq("username", username).execute()
        
        # Debug: Print what we got back
        print(f"Debug - get_user response data: {response.data}")
        print(f"Debug - Data length: {len(response.data) if response.data else 0}")
        
        # Check if we got any data back
        if response.data and len(response.data) > 0:
            user = response.data[0]
            print(f"Debug - Found user: {user}")
            return user  # Return single user object
        else:
            # No user found with that username
            print(f"Debug - No user found with username: {username}")
            return None
            
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
        response = supabase.table("entries").insert(new_entry).execute()
        
        # increase the entry count for the user
        supabase.table("users").update({"entry_count": supabase.table("users").select("entry_count").eq("username", username).execute().data[0]["entry_count"] + 1}).eq("username", username).execute()
        
        print(f"Debug - add_entry response: {response.data}")
        return response.data
        
    except Exception as e:
        print(f"Error adding entry: {e}")
        return None

def get_entries(username: str):
    try:
        # get all entries from the database
        response = supabase.table("entries").select("*").eq("username", username).execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        print(f"Error getting entries: {e}")
        return []

def get_entries_by_date(username: str, date: str):
    try:
        # get all entries from the database
        response = supabase.table("entries").select("*").eq("username", username).eq("created_at", date).execute()
        
        return response.data if response.data else []
        
    except Exception as e:
        print(f"Error getting entries by date: {e}")
        return []

def get_user_streak(username: str):
    try:
        # get the user streak from the database
        response = supabase.table("users").select("streak").eq("username", username).execute()
        
        return response.data[0]["streak"] if response.data else 0
        
    except Exception as e:
        print(f"Error getting user streak: {e}")
        return 0

def update_user_streak(username: str, streak: int):
    try:
        # update the user streak in the database
        response = supabase.table("users").update({"streak": streak}).eq("username", username).execute()
        
        print(f"Debug - update_user_streak response: {response.data}")
        return response.data
        
    except Exception as e:
        print(f"Error updating user streak: {e}")
        return None

def increment_user_entries_count(username: str):
    try:
        # Get current count
        before = supabase.table("users").select("num_entries").eq("username", username).execute()
        
        if not before.data:
            print(f"User {username} not found")
            return False
        
        old_count = before.data[0]["num_entries"] or 0
        new_count = old_count + 1
        
        print(f"Updating {username} from {old_count} to {new_count}")
        
        # Do the update (don't worry about the response)
        supabase.table("users").update({"num_entries": new_count}).eq("username", username).execute()
        
        # Check if it actually changed
        after = supabase.table("users").select("num_entries").eq("username", username).execute()
        actual_count = after.data[0]["num_entries"]
        
        if actual_count == new_count:
            print(f"✅ Success! Count is now {actual_count}")
            return True
        
        else:
            print(f"❌ Failed! Count is still {actual_count}")
            return False
            
    except Exception as e:
        print(f"Error: {e}")
        return False