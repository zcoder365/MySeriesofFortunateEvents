from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gratitude.db' # get the database
db = SQLAlchemy(app) # set up the SQLAlchemy database

# create the user database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    events = db.relationship('Event', backref='user', lazy=True)

# create the event database
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# create all databases
with app.app_context():
    db.create_all()

# landing route
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    
    # get user's entries
    events = Event.query.filter_by(user_id=session['user_id']).order_by(Event.date.desc()).all()
    
    # return the template with the entries retrieved
    return render_template('index.html', events=events)

# add entry route
@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    # if the user isn't login, make the user log in
    if 'user_id' not in session:
        return redirect('/login')
    
    if request.method == 'POST':
        # get the information from the form
        content = request.form['content']
        rating = int(request.form['rating'])
        entry = Event(content=content, rating=rating, user_id=session['user_id'])
        
        # add user to database and save changes
        db.session.add(entry)
        db.session.commit()
        
        # return the home page
        return redirect(url_for('index'))
    
    # if method is GET, return the add entry page
    return render_template('add_entry.html')

# login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # find the user from the database
        user = User.query.filter_by(username=request.form['username']).first()
    
        # if the user exists and the hashed passwords match (the hashed in the database, and the password from the form)
        if user and check_password_hash(user.password, request.form['password']):
            # create the session with the user's ID and return the home route
            session['user_id'] = user.id
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
        
        # find the user
        user = User(username=request.form['username'], password=hashed_password)
        
        # add the user to the database, and commit the changes
        db.session.add(user)
        db.session.commit()
        
        # return the login page so the user can login
        return redirect('/login')
    
    # if the method is GET, return the signup page
    return render_template('signup.html')

# logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None) # remove user from session
    return redirect('/login') # return login page

# mainloop
if __name__ == '__main__':
    app.run(port=8080, debug=True)