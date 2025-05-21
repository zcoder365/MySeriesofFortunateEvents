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

        # check if the user exists
        user = model.find_user(username)
        if not user:
            flash("User does not exist", "danger")
            return redirect(url_for("login"))

        # check if the password is correct
        if not model.login(username, password):
            flash("Incorrect password", "danger")
            return redirect(url_for("login"))

        # set the session
        session["user_id"] = user[0]["id"]
        session["username"] = username

        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        # get info from the form
        username = request.form["username"]
        password = request.form["password"]

        # check if the user exists
        user = model.find_user(username)
        if user:
            flash("User already exists", "danger")
            return redirect(url_for("signup"))

        # add the user to the database
        db.add_user(username, password)

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        # get info from the form
        entry = request.form["entry"]

        # add the entry to the database
        db.add_entry(entry, session["username"])

        return redirect(url_for("home"))

    # get all entries from the database
    entries = db.get_entries(session["username"])

    return render_template("home.html", entries=entries)

@app.route("/add-entry", methods=["GET", "POST"])
def add_entry():
    if request.method == "POST":
        # get info from the form
        entry = request.form["entry"]

        # add the entry to the database
        db.add_entry(entry, session["username"])

        return redirect(url_for("home"))

    return render_template("add-entry.html")

if __name__ == "__main__":
    app.run(port=5001, debug=True)