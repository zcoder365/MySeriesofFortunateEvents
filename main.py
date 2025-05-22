# imports
from flask import Flask, render_template, request, redirect, session, flash, url_for
import utils.model as model
import utils.database as db

# prep the app and add configurations
app = Flask(__name__)
app.config["SECRET_KEY"] = "key"

@app.route("/")
def landing():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # get info from the form
        username = request.form["username"]
        password = request.form["password"]
        
        # Debug: Print what we're trying to log in with
        print(f"Debug - Login attempt with username: '{username}', password: '{password}'")

        # check if the user exists
        user = model.find_user(username)
        print(f"Debug - find_user returned: {user}")
        
        if not user:
            flash("User does not exist", "danger")
            return redirect(url_for("login"))

        # check if the password is correct
        login_result = model.login(username, password)
        print(f"Debug - login result: {login_result}")
        
        if not login_result:
            flash("Incorrect password", "danger")
            return redirect(url_for("login"))
        else:
            # if the password is correct, set the session
            session["user_id"] = user["id"]
            session["username"] = username

            print(f"Debug - Login successful! Session set with user_id: {user['id']}")

            return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # get info from the form
        username = request.form["username"]
        password = request.form["password"]
        
        print(f"Debug - Signup attempt with username: '{username}'")

        # check if the user exists
        user = model.find_user(username)
        if user:
            flash("User already exists", "danger")
            return redirect(url_for("signup"))

        # add the user to the database
        result = db.add_user(username, password)
        print(f"Debug - add_user result: {result}")

        # return the login page
        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/home")
def home():
    # Add session check to prevent accessing home without login
    if "username" not in session:
        flash("Please log in first", "warning")
        return redirect(url_for("login"))

    # get all entries from the database
    entries = db.get_entries(session["username"])

    return render_template("index.html", entries=entries)

@app.route("/add-entry", methods=["GET", "POST"])
def add_entry():
    # Add session check to prevent accessing add-entry without login
    if "username" not in session:
        flash("Please log in first", "warning")
        return redirect(url_for("login"))
        
    if request.method == "POST":
        # get info from the form
        entry = request.form["entry"]

        # add the entry to the database
        db.add_entry(entry, session["username"])

        return redirect(url_for("home"))

    return render_template("add_entry.html")

@app.route("/logout")
def logout():
    # Clear the session when logging out
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(port=5001, debug=True)