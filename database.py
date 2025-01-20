from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# create a mongo client
client = MongoClient("mongodb+srv://zdroulias:FrozenAnna0306@cluster0.h9zxq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# get access to data
db = client['MySeriesOfFortunateEvents']    # connect to the database
users = client.users                        # get the users
events = client.events                      # get the events

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
        "description": event_description,
        "rating": event_rating,
        "user_id": user_id
    }
    
    # insert the document into the database
    events.insert_one(event)