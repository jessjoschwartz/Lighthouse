from flask import Flask, session, request, flash, redirect, url_for, render_template
from model import User, Trip, Status
from model import session as db_session
import datetime
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
    return redirect(url_for("traveler_view_trip"))

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
    return redirect(url_for("traveler_view_trip"))

### Logout
@app.route("/logout")
def logout():
    del session['user_id']
    if 'trip_id' in session:
        del session['trip_id']
    return redirect(url_for("user_login_get"))

### Traveler view
@app.route("/traveler_view_trip", methods=["GET"])
def traveler_view_trip():
    return render_template("traveler_view_trip.html")

@app.route("/traveler_view_trip", methods=["POST"])
def traveler_view_trip_post():

    trip = Trip()
    trip.traveler_id = session['user_id']
    trip.traveler_current_lat = request.form.get('traveler_current_lat')
    trip.traveler_current_long = request.form.get('traveler_current_long')
    trip.traveler_destination_lat = request.form.get('traveler_destination_lat')
    trip.traveler_destination_long = request.form.get('traveler_destination_long')
    trip.traveler_current_address = request.form.get('traveler_current_address')
    trip.traveler_destination_address = request.form.get('traveler_destination_address')

    # Add the user object to the database
    db_session.add(trip)

    # Save the user in the database
    db_session.commit()

    session['trip_id'] = trip.id

    # Confirm
    return 'Success'

@app.route("/traveler_status", methods=["GET"])
def traveler_status():
    if 'trip_id' not in session:
        return ''

    trip_id = session['trip_id']
    status = model.get_status_for_trip(trip_id)
    if status is None:
        return "pending"

    print session['trip_id']
    print status.trip_id
    print status.datetime_accepted
    print status.datetime_commenced
    print status.datetime_completed
    if status.datetime_completed:
        return "completed"
    if status.datetime_commenced:
        return "commenced"
    if status.datetime_accepted:
        return "accepted"
    else: 
        return "pending"



@app.route("/traveler_rate_your_guide", methods=["GET"])
def traveler_rate_your_guide():
    del session['trip_id']
    return render_template("traveler_rate_your_guide.html")

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

@app.route("/guide_view_trip", methods=["GET"])
def guide_view_trip():

    trip_id = request.args.get('id')
    trip = model.get_trip(trip_id)
    session['trip_id'] = trip_id
    return render_template("guide_view_trip.html",
                            trip = trip)
    #request args get from URL, query DB, display 

# @app.route("/guide_accept_voyage", methods=["POST"])
# def guide_accept_voyage():
#     status.trip_id = 
#     status.datetime_accepted = what goes here?

@app.route("/guide_accept_voyage", methods=["POST"])
def guide_accept_voyage():
    trip_id = session['trip_id']

    status = Status()
    status.trip_id = trip_id
    status.datetime_accepted = datetime.datetime.now()

    # Add the user object to the database
    db_session.add(status)

    # Save the user in the database
    db_session.commit()

    # Confirm
    return render_template("guide_commence_voyage.html")

@app.route("/guide_commence_voyage", methods=["POST"])
def guide_commence_voyage():
    trip_id = session['trip_id']
    status = model.get_status_for_trip(trip_id)
    status.datetime_commenced = datetime.datetime.now()

    # Add the user object to the database
    db_session.merge(status)

    # Save the user in the database
    db_session.commit()

    return render_template("guide_complete_voyage.html")

@app.route("/guide_complete_voyage", methods=["POST"])
def guide_complete_voyage():

    trip_id = session['trip_id']
    status = model.get_status_for_trip(trip_id)
    status.datetime_completed = datetime.datetime.now()

    # Add the user object to the database
    db_session.merge(status)

    # Save the user in the database
    db_session.commit()
    del session['trip_id']

    return url_for("guide_rate_your_traveler")

@app.route("/guide_rate_your_traveler", methods=["GET"])
def guide_rate_your_traveler():
    return render_template("guide_rate_your_traveler.html")

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