from pymongo import MongoClient

# create a mongo client
client = MongoClient("mongodb+srv://zdroulias:FrozenAnna0306@cluster0.h9zxq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# get access to data
client.MySeriesOfFortunateEvents    # connect to the database
users = client.users                # get the users
events = client.events              # get the events

# USER FUNCTIONS
def find_user(username: str):
    pass

def add_user(username: str, password: str):
    pass

# EVENT FUNCTIONS
def create_event(event_description: str, event_rating: int):
    pass