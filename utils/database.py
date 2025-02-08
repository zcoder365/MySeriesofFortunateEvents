import sqlite3

DB_PATH = 'data/fortunate_events.db'

def create_db():
    try:
        # create connection to and cursor for the database
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        
        # create tables
        c.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            );
            
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                rating INTEGER NOT NULL,
                date TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # commit the changes
        conn.commit()
    except sqlite3.Error as e:
        print("Error creating database: ", e)
    finally:
        # close the connection
        if conn:
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

def get_events(user_id):
    # connect to the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # get the events from the database
    c.execute('''
        SELECT * FROM events WHERE user_id = ?
    ''', (user_id,))
    events = c.fetchall()
    
    # close the connection
    conn.close()
    
    return events

def get_entry_by_date(user_id, date):
    # connect to the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # get the event from the database
    c.execute('''
        SELECT * FROM events WHERE user_id = ? AND date = ?
    ''', (user_id, date))
    event = c.fetchone()
    
    # close the connection
    conn.close()
    
    # return the event
    return event