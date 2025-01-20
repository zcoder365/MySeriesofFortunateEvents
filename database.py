from pymongo import MongoClient

# create a mongo client
client = MongoClient("mongodb+srv://zdroulias:FrozenAnna0306@cluster0.h9zxq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# connect to the database
client.MySeriesOfFortunateEvents
users = client.users
events = client.events