import sqlite3

DB_PATH = 'data/fortunate_events.db'

def create_db():
    # create connection to and cursor for the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # create tables
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
        
        CREATE TABLE events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            rating INTEGER NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    
    # close the connection
    conn.commit()
    conn.close()

def create_user(username, password):
    # connect to the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # insert the user into the database
    c.execute('''
        INSERT INTO users (username, password)
        VALUES (?, ?)
    ''', (username, password))
    
    # commit changes and close the connection
    conn.commit()
    conn.close()
    
def get_user(username):
    # connect to the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # get the user from the database
    c.execute('''
        SELECT * FROM users WHERE username = ?
    ''', (username,))
    user = c.fetchone()
    
    # close the connection
    conn.close()
    
    return user

def create_event(user_id, title, rating, date):
    # connect to the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # insert the event into the database
    c.execute('''
        INSERT INTO events (user_id, title, rating, date)
        VALUES (?, ?, ?, ?)
    ''', (user_id, title, rating, date))
    
    # commit changes and close the connection
    conn.commit()
    conn.close()