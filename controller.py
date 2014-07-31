from flask import Flask, session, request, flash, redirect, url_for, render_template
from model import User, Trip
from model import session as db_session
import model
import os
import pdb

app = Flask(__name__)
SECRET_KEY = "fish"
app.config.from_object(__name__)

@app.before_request
def is_logged_in():

    session['is_login_required'] = is_login_required()

    if not 'user_id' in session and is_login_required():
        return redirect(url_for("user_login_get"))

def is_login_required():
    pages = ["/login", "/register", "/"]
    if request.path in pages:
        return False
    else:
        return True 

### Start page
@app.route("/", methods=["GET"])
def display_start():
    return render_template("start.html")

### User login
@app.route("/login", methods=["GET"])
def user_login_get():
    return render_template("user_login.html")

@app.route("/login", methods=["POST"])
def user_login_post():
    email = request.form['email']
    password = request.form['password']

    try:
        user = db_session.query(User).filter_by(email=email).filter_by(password=password).one()
    except:
        flash("Invalid username or password", "error")
        return redirect(url_for("user_login_get"))

    session['user_id'] = user.id
    return redirect(url_for("traveler_view"))

### Registration page

@app.route("/register", methods=["GET"])
def register_get():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register_post():

    # Create the user object to store our data
    user = User()
    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.email = request.form.get('email')
    user.phone = request.form.get('phone')
    user.password = request.form.get('password')
    user.role = request.form.get('role')

    existing = db_session.query(User).filter_by(email=user.email).first()
    if existing:
        flash("Email already in use", "error")
        return redirect(url_for("user_login_get"))


    # Add the user object to the database
    db_session.add(user)

    # Save the user in the database
    db_session.commit()

    # session['user_id'] = user.id

    # # save photo with user id as filename (1.jpg)

    #Log in user


    # # Redirect user to landing page
    return redirect(url_for("traveler_view_request"))

### Logout
@app.route("/logout")
def logout():
    del session['user_id']
    return redirect(url_for("user_login_get"))

### Traveler view
@app.route("/traveler_view_request", methods=["GET"])
def traveler_view_request():
    return render_template("traveler_view_request.html")

@app.route("/traveler_view_request", methods=["POST"])
def traveler_view_request_post():

    trip = Trip()
    trip.traveler_id = session['user_id']
    trip.traveler_current_lat = request.form.get('traveler_current_lat')
    trip.traveler_current_long = request.form.get('traveler_current_long')
    trip.traveler_destination_lat = request.form.get('traveler_destination_lat')
    trip.traveler_destination_long = request.form.get('traveler_destination_long')

    # Add the user object to the database
    db_session.add(trip)

    # Save the user in the database
    db_session.commit()

    # Confirm
    return 'Success'
    return redirect(url_for("traveler_view_trip"))

@app.route("/traveler_view_trip", methods=["GET"])
def traveler_view_trip():
    return render_template("traveler_view_trip.html")

@app.route("/traveler_status", methods=["GET"])
def traveler_status():
    return "commenced" 

### Guide view
@app.route("/guide_view_ahoy", methods=["GET"])
def guide_view_ahoy():
    return render_template("guide_view_ahoy.html")

@app.route("/guide_view_ahoy", methods=["POST"])
def guide_view_ahoy_post():

    trip = Trip()
    trip.guide_id = session['user_id']
    trip.guide_current_lat = request.form.get('guide_current_lat')
    trip.guide_current_long = request.form.get('guide_current_long')
    print trip.guide_current_lat

    # # Add the user object to the database
    # db_session.add(trip)

    # # Save the user in the database
    # db_session.commit()

    # Confirm
    # return 'Success'
    return redirect(url_for("guide_available_trips"))

@app.route("/guide_available_trips", methods=["GET"])
def guide_available_trips():
    # users = model.get_trips()
    # print users
    trips = model.get_trips()
    print trips
    return render_template("guide_available_trips.html",
                           trip_list = trips)

# @app.route("/accept_voyage", methods=["POST"])
# def accept_voyage():
#     return render_template("commence_voyage.html")

# @app.route("/cancel_voyage", methods=["POST"])
# def cancel_voyage():
#     return render_template("commence_voyage.html")

@app.route("/guide_view_trip", methods=["GET"])
def guide_view_accept():
    return render_template("guide_view_trip.html")

@app.route("/guide_commence_voyage", methods=["POST"])
def guide_commence_voyage():
    return render_template("guide_commence_voyage.html")

@app.route("/guide_complete_voyage", methods=["POST"])
def guide_complete_voyage():
    return render_template("guide_complete_voyage.html")

@app.route("/guide_rate_your_traveler", methods=["GET"])
def guide_rate_your_traveler():
    return render_template("guide_rate_your_traveler.html")

# @app.route("/voyage_confirmed", methods=["POST"])
# def voyage_confirmed():
#     return "<p style='color:red;font-size:72px;' id='new-p'>HELLO WORLD 4</p>"

# @app.route("/voyage_commenced", methods=["POST"])
# def voyage_commenced():
#     return "<p style='color:red;font-size:72px;' id='new-p'>HELLO WORLD 4</p>"

# @app.route("/voyage_complete", methods=["POST"])
# def voyage_complete():
#     return "<p style='color:red;font-size:72px;' id='new-p'>HELLO WORLD 4</p>"


## End class declarations

def main():
    """In case we need this for something"""
    pass    

if __name__ == "__main__":
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if not db_uri:
        db_uri = "sqlite:///users.db"
    model.connect(db_uri)
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host="0.0.0.0")