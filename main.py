# imports
from flask import Flask, render_template, request, redirect, session, flash, url_for
from datetime import datetime
from database import find_user, add_user, create_event  # Import the MongoDB functions

# prep the app and add configurations
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session management

# landing route
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    
    # get user's entries from MongoDB events collection
    # Note: In MongoDB, we'll query events by user_id directly
    events = events.find({"user_id": session['user_id']}).sort("date", -1)
    
    # return the template with the entries retrieved
    return render_template('index.html', events=events)

# add entry route
@app.route('/add-entry', methods=['GET', 'POST'])
def add_entry():
    # if the user isn't login, make the user log in
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        # get the information from the form
        content = request.form['content']
        rating = int(request.form['rating'])
        
        # create an event entry using MongoDB function
        create_event(
            user_id=session['user_id'],
            event_description=content,
            event_rating=rating
        )
        
        # return the home page
        return redirect(url_for('index'))
    
    # if method is GET, return the add entry page
    return render_template('add_entry.html')

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # find the user from MongoDB using the imported function
        user = find_user(request.form['username'])
    
        # if the user exists and the hashed passwords match
        if user and check_password_hash(user['password'], request.form['password']):
            # create the session with the user's ID and return the home route
            session['user_id'] = str(user['_id'])  # MongoDB uses ObjectId, convert to string
            return redirect(url_for('index'))
    
        # flash error message for incorrect username or password
        flash('Invalid username or password')
    
    # if the method is GET, return the login page
    return render_template('login.html')

# signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # hash the password
        hashed_password = generate_password_hash(request.form['password'])
        
        # Check if username already exists
        existing_user = find_user(request.form['username'])
        if existing_user:
            flash('Username already exists')
            return redirect('/signup')
        
        # add the user using MongoDB function
        add_user(
            username=request.form['username'],
            password=hashed_password
        )
        
        # return the login page so the user can login
        return redirect('/login')
    
    # if the method is GET, return the signup page
    return render_template('signup.html')

# logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # remove user from session
    return redirect('/login')     # return login page

# mainloop
if __name__ == '__main__':
    app.run(debug=True)