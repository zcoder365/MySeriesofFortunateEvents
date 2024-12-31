import sqlite3
from datetime import datetime

# Initialize database connection
def init_db():
    conn = sqlite3.connect("user_events.db")
    cursor = conn.cursor()
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    # Create events table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            event TEXT,
            rating INTEGER,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

# User registration
def register_user():
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    try:
        conn = sqlite3.connect("user_events.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        print("Registration successful!\n")
    except sqlite3.IntegrityError:
        print("Username already exists. Try a different one.\n")
    finally:
        conn.close()

# User login
def login_user():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    conn = sqlite3.connect("user_events.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        print("Login successful!\n")
        return user[0]  # Return user_id
    else:
        print("Invalid username or password.\n")
        return None

# Log an event
def log_event(user_id):
    sentence = input("Write a sentence about a good event that happened: ")
    while True:
        try:
            rating = int(input("Rate this event out of 10: "))
            if 0 <= rating <= 10:
                break
            else:
                print("Rating must be between 0 and 10.")
        except ValueError:
            print("Please enter a valid number.")

    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect("user_events.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO events (user_id, date, event, rating) VALUES (?, ?, ?, ?)", (user_id, date, sentence, rating))
    conn.commit()
    conn.close()
    print("Event logged successfully!\n")

# View logged events
def view_events(user_id):
    conn = sqlite3.connect("user_events.db")
    cursor = conn.cursor()
    cursor.execute("SELECT date, event, rating FROM events WHERE user_id = ?", (user_id,))
    events = cursor.fetchall()
    conn.close()

    if events:
        print("\nYour Events:")
        for event in events:
            print(f"Date: {event[0]}\nEvent: {event[1]}\nRating: {event[2]}/10\n")
    else:
        print("\nNo events logged yet.\n")