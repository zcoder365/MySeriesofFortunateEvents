# imports
from flask import Flask, render_template, request, redirect, session, flash, url_for
from datetime import datetime, timedelta

# import files from utils directory
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
            session["user_id"] = str(user["_id"])  # FIX: MongoDB uses _id, convert to string
            session["username"] = username

            print(f"Debug - Login successful! Session set with user_id: {user['_id']}")

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
    if "username" not in session:
        flash("Please log in first", "warning")
        return redirect(url_for("login"))

    # get all entries from the database
    entries = db.get_entries(session["username"])
    # Sort by date (assuming MM/DD/YYYY format)
    try:
        entries_sorted = sorted(
            entries,
            key=lambda e: datetime.strptime(e["created_at"], "%m/%d/%Y"),
            reverse=True
        )
    except Exception:
        entries_sorted = entries[::-1]  # fallback: reverse order

    # Pagination
    limit = int(request.args.get("limit", 50))
    show_more = len(entries_sorted) > limit
    entries_display = entries_sorted[:limit]

    return render_template(
        "index.html",
        entries=entries_display,
        show_more=show_more,
        next_limit=limit + 50
    )

@app.route("/add-entry", methods=["GET", "POST"])
def add_entry():
    if "username" not in session:
        flash("Please log in first", "warning")
        return redirect(url_for("login"))
        
    if request.method == "POST":
        entry = request.form["entry"]
        rating = request.form["rating"]
        username = session["username"]
        
        # check if the user already made an entry today
        today = datetime.today().strftime('%Y-%m-%d')
        # FIX: get_entries_by_date should match entries for the day, not exact datetime string
        entries_today = [
            e for e in db.get_entries(username)
            if e.get("created_at", "").startswith(today)
        ]
        is_first_entry_today = len(entries_today) == 0

        db.add_entry(entry, rating, username)
        
        if is_first_entry_today:
            model.update_streak(username)
            flash("Streak updated!", "success")
            
        db.increment_user_entries_count(username)

        return redirect(url_for("home"))

    return render_template("add_entry.html")

@app.route("/my-profile")
def my_profile():
    if "username" not in session:
        flash("Please log in first", "warning")
        return redirect(url_for("login"))

    user = model.find_user(session["username"])
    if not user:
        flash("User not found", "danger")
        return redirect(url_for("login"))
    
    username = user["username"]
    streak = user.get("streak", 0)
    num_entries = user.get("num_entries", 0)

    # Get last 7 entries for "Best this week" chart
    entries = db.get_entries(username)
    # Count ratings from 1 to 10
    rating_counts = {str(i): 0 for i in range(1, 11)}
    for e in entries:
        rating = str(e.get("rating"))
        if rating in rating_counts:
            rating_counts[rating] += 1

    chart_labels = list(rating_counts.keys())  # ["1", "2", ..., "10"]
    chart_data = list(rating_counts.values())  # [count for 1, count for 2, ..., count for 10]

    # Filter entries from the last 30 days
    today = datetime.today()
    month_entries = []
    for e in entries:
        try:
            entry_date = datetime.strptime(e["created_at"], "%m/%d/%Y")
            if (today - entry_date).days < 30:
                month_entries.append(e)
        except Exception:
            continue

    # Count ratings from 1 to 10 for the last month
    rating_counts_month = {str(i): 0 for i in range(1, 11)}
    for e in month_entries:
        rating = str(e.get("rating"))
        if rating in rating_counts_month:
            rating_counts_month[rating] += 1

    chart_labels_month = list(rating_counts_month.keys())
    chart_data_month = list(rating_counts_month.values())

    return render_template(
        "profile.html", 
        username=username, 
        streak=streak, 
        num_entries=num_entries,
        chart_labels=chart_labels,
        chart_data=chart_data,
        chart_labels_month=chart_labels_month,
        chart_data_month=chart_data_month
    )

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out", "info")
    return redirect(url_for("login"))

@app.route("/search-entries", methods=["GET", "POST"])
def search_entries():
    if "username" not in session:
        flash("Please log in first", "warning")
        return redirect(url_for("login"))

    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if query:
            # Use the new search_user_entries function from database.py
            results = db.search_user_entries(session["username"], query)
        else:
            flash("Please enter a search term.", "warning")

    return render_template("search-entries.html", results=results, query=query)

if __name__ == "__main__":
    app.run(port=5001, debug=True)