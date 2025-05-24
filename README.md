# My Series of Fortunate Events
A Flask-based web application that encourages daily reflection by allowing users to record daily events and rate their positivity on a scale of 1-10. Track your streak of consecutive days and build a habit of focusing on the positive moments in life.

# Features

- **User Authentication:** Secure signup and login system with bcrypt password hashing
- **Daily Entries:** Record what happened each day with a text description and positivity rating (1-10)
- **Streak Tracking:** Maintain a streak counter for consecutive days of entries
- **User Profile:** View personal statistics including username, current streak, and total entries
- **Responsive Design:** Clean, colorful UI with a friendly Comic Sans font and warm color palette
- **Session Management:** Secure session handling with logout functionality

# Tech Stack

- **Backend:** Python Flask
- **Database:** Supabase (PostgreSQL)
- **Frontend:** HTML5, CSS3, Jinja2 templating
- **Authentication:** bcrypt for password hashing
- **Environment:** Python dotenv for configuration


# Project Structure
```
MySeriesofFortunateEvents/
├── main.py                 # Main Flask application with routes
├── utils/
│   ├── database.py        # Database operations and Supabase client
│   └── model.py           # Business logic and data models
├── templates/
│   ├── base.html          # Base template with navigation
│   ├── login.html         # User login form
│   ├── signup.html        # User registration form
│   ├── index.html         # Home page displaying user entries
│   ├── add_entry.html     # Form for adding new daily entries
│   └── profile.html       # User profile with statistics
├── static/
│   ├── styles.css         # Main stylesheet with CSS custom properties
│   └── assets/
│       └── logo.png       # Application logo
└── .env                   # Environment variables (not tracked)
```

# Key Functions
## Authentication System

- `login()`: Handles user authentication with bcrypt password verification
- `signup()`: Creates new user accounts with hashed passwords
Session management prevents unauthorized access to protected routes

## Entry Management

add_entry(): Creates new daily entries and updates user statistics
get_entries(): Retrieves all entries for the logged-in user
Streak logic: Only increments streak on the first entry of each day

## Database Operations

Secure password hashing with bcrypt
Error handling for database operations
Automatic user statistics updates (entry count, streak tracking)

## Todo
- [ ] Add a bar chart to profile page for visualizing entry ratings over time
- [ ] Implement entry search and filtering