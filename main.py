from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# create the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = "key" # change this to a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///events.db" # change?
db = SQLAlchemy(app) # create the database

# database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    events = db.relationship('Event', backref='user', lazy=True)

class Event:
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# routes
@app.route('/')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    events = Event.query.filter_by(user_id=session['user_id']).order_by(Event.date.desc()).all()
    
    return render_template("home.html", events=events, username=user.username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return redirect(url_for('home'))
        
        flash('Invalid username or password')
    
    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists")
            return redirect(url_for('register'))
        
        # hash the password
        hashed_pw = generate_password_hash(password)
        
        # create a new user instance
        new_user = User(username, hashed_pw)
        
        # add the user to the database
        db.session.add(new_user)
        db.session.commit()
        
        flash("Registration successful! Please login.")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/add_event', methods=['POST'])
def add_event():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    text = request.form['event_text']
    rating = request.form['rating']
    
    if not text or not rating:
        flash('Please fill in all fields')
        return redirect(url_for('home'))
    
    try:
        rating = int(rating)
        if not 1 <= rating <= 10:
            raise ValueError
    
    except ValueError:
        flash('Rating must be a number between 1 and 10')
        return redirect(url_for('home'))
    
    new_event = Event(text=text, rating=rating, user_id=session['user_id'])
    db.session.add(new_event)
    db.session.commit()
    
    flash('Event added successfully!')
    
    return redirect(url_for('home'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)