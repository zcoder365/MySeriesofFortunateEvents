from supabase import create_client, Client
import os
from dotenv import load_dotenv
import bcrypt

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
            "username": username
        }
        
        # add an entry to the database
        response = supabase.table("entries").insert(new_entry).execute()
        
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