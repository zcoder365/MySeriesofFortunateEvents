from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson.objectid import ObjectId

# create a mongo client
client = MongoClient("mongodb+srv://zdroulias:FrozenAnna0306@cluster0.h9zxq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# get access to data
db = client['MySeriesOfFortunateEvents']    # connect to the database
users = client.users                        # get the users
events = client.events                      # get the events

# SECURITY FUNCTIONS
def check_password(password_hash: str, password: str):
    return check_password_hash(password_hash, password)

def hash_password(password: str):
    return generate_password_hash(password)

# USER FUNCTIONS
def find_user(username: str):
    return users.find_one({"username": username})

def add_user(username: str, password: str):
    user = {
        "username": username,
        "password": password
    }
    
    users.insert_one(user)

# EVENT FUNCTIONS
def create_event(user_id: str, event_description: str, event_rating: int):
    # get today's date
    today = datetime.today()
    
    # create an event document
    event = {
        "date": today,
        "description": event_description,
        "rating": event_rating,
        "user_id": user_id
    }
    
    # insert the document into the database
    return events.insert_one(event)

def get_events(user_id: str):
    return events.find({"_id": ObjectId(user_id)})

def check_entries(user_id: str):
    # get all entries for the user
    entries = get_events(user_id)