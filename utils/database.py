from supabase import create_client, Client
import os
from dotenv import load_dotenv

# load the environment variables from the .env file
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

# create a client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# USER FUNCTIONS
# add a user to the database
def add_user(username: str, password: str):
    # create a user entry
    new_user_entry = {
        "username": username,
        "password": password
    }
    
    # add a user to the database
    response = supabase.table("users").insert(new_user_entry).execute()
    
    if response.error:
        print("Error adding user:", response.error)
        return None
    
    return response.data

# get a user from the database
def get_user(username: str):
    # get a user from the database
    response = supabase.table("users").select("*").eq("username", username).execute()
    
    if response.error:
        print("Error getting user:", response.error)
        return None
    
    return response.data