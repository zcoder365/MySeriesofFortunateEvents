from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gratitude.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    entries = db.relationship('Entry', backref='user', lazy=True)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    
    # get user and their entries
    # user = User.query.get(session['user_id'])
    entries = Entry.query.filter_by(user_id=session['user_id']).order_by(Entry.date.desc()).all()
    
    # return the template with the entries retrieved
    return render_template('index.html', entries=entries)

@app.route('/add_entry', methods=['GET', 'POST'])
def add_entry():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        content = request.form['content']
        rating = int(request.form['rating'])
        entry = Entry(content=content, rating=rating, user_id=session['user_id'])
        db.session.add(entry)
        db.session.commit()
        return redirect('/')
    return render_template('add_entry.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            session['user_id'] = user.id
            return redirect('/')
        flash('Invalid username or password')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'])
        user = User(username=request.form['username'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

# mainloop
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)