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