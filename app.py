import folium
import base64
import branca.element

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required
from datetime import datetime
from geocodio import GeocodioClient
from geopy.distance import geodesic


# Configure application
app = Flask(__name__)

# Configure Geocodio Client
client = GeocodioClient("09d330c4f9f94cd6a249e3003faae0ed0c99466")


EVENT_CATEGORIES = [
    "Music",
    "Food",
    "Sport",
    "Festival"
]

# Configure session to use the filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")

@app.after_request
def after_request(response):
    """Ensure responses are not cached"""
    response.headers["Cache-Control"] = "no-cache no-store must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    return render_template("index.html")


@app.route("/add_event", methods=["GET", "POST"])
@login_required
def add_event():
    user_id = session["user_id"]
    if request.method == "POST":
        category = request.form.get("category")
        title = request.form.get("title")
        description = request.form.get("description")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        address = request.form.get("address")

        geocoded_location = client.geocode(address)
        lat = geocoded_location.coords[0]
        lon = geocoded_location.coords[1]

        users = db.execute("SELECT * FROM users")

        for user in users:
            if user["id"] == user_id:
                db.execute("INSERT INTO events (category, title, description, start_time, end_time, address, latitude, longitude, event_creator_id, time_created) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", category, title, description, start_time, end_time, address, lat, lon, user_id, datetime.now())
                flash("Event has been added", "success")
        return redirect("/")

    else:
        return render_template("add_event.html", categories=EVENT_CATEGORIES)


@app.route("/all_events")
@login_required
def all_events():
    # Show ALL events
    all_locations = db.execute("SELECT * FROM events")

    # Initialize list for location data
    map_grp = []
    for location in all_locations:
        location_lat = location["latitude"]
        location_lon = location["longitude"]
        location_title = location["title"]
        location_desc = location["description"]
        location_address = location["address"]

        # convert datetime's to UTC for better iFrame appearance
        start_iso = location["start_time"]
        start_utc = datetime.fromisoformat(start_iso)
        end_iso = location["end_time"]
        end_utc = datetime.fromisoformat(end_iso)

        # Data to be appended to the list (map_grp)
        location_grp = (location_lat, location_lon, location_title, location_desc, location_address, start_utc, end_utc)

        map_grp.append(location_grp)

    if map_grp:
        # Create a Folium map object, centered at a general location
        # The tiles='OpenStreetMap' is used by default, no API key needed
        m = folium.Map(location=[location_lat, location_lon], zoom_start=4)
        file_path = "/workspaces/255863923/project/static/portaplotta_nav.png"
        # Image must be encoded for proper rendering
        encoded = base64.b64encode(open(file_path, 'rb').read()).decode('UTF-8')

        # Add markers for each location
        for lat, lon, title, desc, address, start, end in map_grp:
            html = f"""<img src="data:image/png;base64,{encoded}" style="float: left; width: 250; height: auto; margin: 0;">
                <h1>{title}</h1><p style="font-size: 18px;">
                Description: {desc}<br>
                Address: {address}<br>
                Start time: {start}<br>
                End Time: {end}</p>"""

            iframe = branca.element.IFrame(html=html, width=620, height=220)
            popup = folium.Popup(iframe, max_width=620)

            folium.Marker([lat, lon],
            popup=popup,
            tooltip='Click for more info',
            icon=folium.Icon(color='green', icon='info-sign')).add_to(m)

        # Render the map to an HTML string
        map_html = m._repr_html_()

        # Pass the HTML string to the Flask template
        return render_template('map_page.html', map_html=map_html, map_grp=map_grp)

    else:
        return render_template("error.html", message="There are no event records to display.")


@app.route("/delete_account", methods=["GET", "POST"])
@login_required
def delete_account():
    user_id = session["user_id"]
    if request.method == "POST":
        answer = request.form.get("answer")
        if answer == "yes":
            db.execute("DELETE FROM users WHERE id = ?", user_id)
            flash("Account deleted.")

        return redirect("/logout")

    else:
        return render_template("delete_account.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html", message="Must provide username.")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html", message="Must provide password.")

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["password_hash"], request.form.get("password")
        ):
            return render_template("error.html", message="Invalid name and/or password.")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        flash("You are now logged in.", "success")
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("You have been logged out.", "success")
    return redirect("/")


@app.route("/pong")
@login_required
def pong():
    return render_template('pong.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    # """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        try:
            # Ensure username was submitted
            username = request.form.get("username")
            if not username:
                return render_template("error.html", message="Please enter a username.")

            # Ensure password was submitted
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")
            if not password:
                return render_template("error.html", message="Password field must not be blank.")
            if not confirmation:
                return render_template("error.html", message="Confirmation field must not be blank.")
            if confirmation != password:
                return render_template("error.html", message="Passwords do not match.")
            hPassword = generate_password_hash(password)
            db.execute("INSERT INTO users (username, password_hash) VALUES(?, ?)", username, hPassword)

        except ValueError:
            return render_template("error.html", message="Please use another username.")

        flash("You are now registered", "success")
        return render_template("login.html")

    else:
        return render_template("register.html")


@app.route("/search_event", methods=["GET", "POST"])
@login_required
def search_event():

    if request.method == "POST":
        # Data from the form
        SEARCH_RADIUS_KM = request.form.get("search_radius")
        user_lat = request.form.get("latitude")
        user_lon = request.form.get("longitude")
        TARGET_COORDS = (user_lat, user_lon)

        all_locations = db.execute("SELECT * FROM events")

        locations_within_radius = []
        map_grp = []
        for location in all_locations:
            location_lat = location["latitude"]
            location_lon = location["longitude"]
            location_title = location["title"]
            location_desc = location["description"]
            location_address = location["address"]

            start_iso = location["start_time"]
            start_utc = datetime.fromisoformat(start_iso)

            end_iso = location["end_time"]
            end_utc = datetime.fromisoformat(end_iso)

            location_coords = (location_lat, location_lon)
            location_grp = (location_lat, location_lon, location_title, location_desc, location_address, start_utc, end_utc)

            # Calculate distance in KM
            distance = geodesic(TARGET_COORDS, location_coords).km

            if distance <= float(SEARCH_RADIUS_KM):
                locations_within_radius.append(location_grp)

           # map_grp.append(location_grp)
          #  session["map_grp"] = map_grp

        if locations_within_radius:
            # Create a Folium map object, centered at a general location
            # The tiles='OpenStreetMap' is used by default, no API key needed
            m = folium.Map(location=[user_lat, user_lon], zoom_start=4)
            file_path = "/workspaces/255863923/project/static/portaplotta_nav.png"
            # Image must be encoded for proper rendering
            encoded = base64.b64encode(open(file_path, 'rb').read()).decode('UTF-8')

            # Add markers for each location
            for lat, lon, title, desc, address, start, end in locations_within_radius:
                html = f"""<img src="data:image/png;base64,{encoded}" style="float: left; width: 250; height: auto; margin: 0;">
                    <h1>{title}</h1><p style="font-size: 18px;">
                    Description: {desc}<br>
                    Address: {address}<br>
                    Start time: {start}<br>
                    End Time: {end}</p>"""

                iframe = branca.element.IFrame(html=html, width=620, height=220)
                popup = folium.Popup(iframe, max_width=620)

                folium.Marker([lat, lon],
                popup=popup,
                tooltip='Click for more info',
                icon=folium.Icon(color='green', icon='info-sign')).add_to(m)

            # Render the map to an HTML string
            map_html = m._repr_html_()

            # Pass the HTML string to the Flask template
            return render_template('map_page.html', map_html=map_html, map_grp=map_grp)

        else:
            return render_template("error.html", message="There are no records to display. Try increasing the search proximity.")

    else:
        return render_template("search_event.html")











