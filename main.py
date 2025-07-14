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

    entries = db.get_entries(username)
    today = datetime.today()

    # --- WEEK STATS --- (your existing code)
    week_entries = []
    for e in entries:
        try:
            entry_date = datetime.strptime(e["created_at"], "%m/%d/%Y")
            if (today - entry_date).days < 7:
                week_entries.append(e)
        except Exception:
            continue

    week_ratings = [int(e.get("rating", 0)) for e in week_entries if e.get("rating")]
    week_total_entries = len(week_ratings)
    week_avg_rating = round(sum(week_ratings) / week_total_entries, 2) if week_total_entries else "N/A"
    week_max_rating = max(week_ratings) if week_ratings else "N/A"
    week_min_rating = min(week_ratings) if week_ratings else "N/A"

    week_rating_counts = {str(i): 0 for i in range(1, 11)}
    for r in week_ratings:
        if str(r) in week_rating_counts:
            week_rating_counts[str(r)] += 1
    chart_labels = list(week_rating_counts.keys())
    chart_data = list(week_rating_counts.values())

    # --- MONTH STATS --- (your existing code)
    month_entries = []
    for e in entries:
        try:
            entry_date = datetime.strptime(e["created_at"], "%m/%d/%Y")
            if (today - entry_date).days < 30:
                month_entries.append(e)
        except Exception:
            continue

    month_ratings = [int(e.get("rating", 0)) for e in month_entries if e.get("rating")]
    month_total_entries = len(month_ratings)
    month_avg_rating = round(sum(month_ratings) / month_total_entries, 2) if month_total_entries else "N/A"
    month_max_rating = max(month_ratings) if month_ratings else "N/A"
    month_min_rating = min(month_ratings) if month_ratings else "N/A"

    month_rating_counts = {str(i): 0 for i in range(1, 11)}
    for r in month_ratings:
        if str(r) in month_rating_counts:
            month_rating_counts[str(r)] += 1
    chart_labels_month = list(month_rating_counts.keys())
    chart_data_month = list(month_rating_counts.values())

    # --- ADD THIS: ALL TIME STATS ---
    # Get all ratings from all entries
    all_ratings = [int(e.get("rating", 0)) for e in entries if e.get("rating")]
    all_total_entries = len(all_ratings)
    all_avg_rating = round(sum(all_ratings) / all_total_entries, 2) if all_total_entries else "N/A"
    all_max_rating = max(all_ratings) if all_ratings else "N/A"
    all_min_rating = min(all_ratings) if all_ratings else "N/A"

    # Histogram for all time - count how many entries have each rating (1-10)
    all_rating_counts = {str(i): 0 for i in range(1, 11)}
    for r in all_ratings:
        if str(r) in all_rating_counts:
            all_rating_counts[str(r)] += 1
    chart_labels_all = list(all_rating_counts.keys())
    chart_data_all = list(all_rating_counts.values())
    
    # --- YEARLY REVIEW STATS ---
    # Get current year
    current_year = datetime.today().year

    # Initialize monthly data for the year
    monthly_averages = {}
    monthly_counts = {}
    for month in range(1, 13):
        monthly_averages[month] = 0
        monthly_counts[month] = 0

    # Process entries for yearly review
    for e in entries:
        try:
            # Parse the date (assuming MM/DD/YYYY format)
            entry_date = datetime.strptime(e["created_at"], "%m/%d/%Y")
            if entry_date.year == current_year and e.get("rating"):
                month = entry_date.month
                rating = int(e.get("rating", 0))
                if monthly_counts[month] == 0:
                    monthly_averages[month] = rating
                    monthly_counts[month] = 1
                else:
                    # Calculate running average
                    total = monthly_averages[month] * monthly_counts[month] + rating
                    monthly_counts[month] += 1
                    monthly_averages[month] = total / monthly_counts[month]
        except Exception:
            continue

    # Prepare data for chart (month names and averages)
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    yearly_labels = month_names
    yearly_data = [round(monthly_averages[i], 2) if monthly_counts[i] > 0 else 0 
                for i in range(1, 13)]
    yearly_counts = [monthly_counts[i] for i in range(1, 13)]

    # Calculate yearly stats
    year_entries_with_ratings = [monthly_counts[i] for i in range(1, 13) if monthly_counts[i] > 0]
    year_ratings_list = [monthly_averages[i] for i in range(1, 13) if monthly_counts[i] > 0]

    yearly_total_entries = sum(yearly_counts)
    yearly_avg_rating = round(sum(year_ratings_list) / len(year_ratings_list), 2) if year_ratings_list else "N/A"
    yearly_max_rating = round(max(year_ratings_list), 2) if year_ratings_list else "N/A"
    yearly_min_rating = round(min(year_ratings_list), 2) if year_ratings_list else "N/A"

    # Update your return statement to include ALL the variables
    return render_template(
        "profile.html", 
        username=username, 
        streak=streak, 
        num_entries=num_entries,
        # Week data
        chart_labels=chart_labels,
        chart_data=chart_data,
        week_avg_rating=week_avg_rating,
        week_max_rating=week_max_rating,
        week_min_rating=week_min_rating,
        week_total_entries=week_total_entries,
        # Month data
        chart_labels_month=chart_labels_month,
        chart_data_month=chart_data_month,
        month_avg_rating=month_avg_rating,
        month_max_rating=month_max_rating,
        month_min_rating=month_min_rating,
        month_total_entries=month_total_entries,
        # ALL TIME data - ADD THESE
        chart_labels_all=chart_labels_all,
        chart_data_all=chart_data_all,
        all_avg_rating=all_avg_rating,
        all_max_rating=all_max_rating,
        all_min_rating=all_min_rating,
        all_total_entries=all_total_entries,
        
        # Add these new variables for yearly chart
        chart_labels_yearly=yearly_labels,
        chart_data_yearly=yearly_data,
        chart_counts_yearly=yearly_counts,
        current_year=current_year,
        yearly_avg_rating=yearly_avg_rating,
        yearly_max_rating=yearly_max_rating,
        yearly_min_rating=yearly_min_rating,
        yearly_total_entries=yearly_total_entries
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

@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    if "username" not in session:
        flash("Please log in first", "warning")
        return redirect(url_for("login"))
    if request.method == "POST":
        # Implement your password reset logic here
        flash("Password reset functionality coming soon!", "info")
        return redirect(url_for("my_profile"))
    return render_template("reset-password.html")

if __name__ == "__main__":
    app.run(port=5001, debug=True)