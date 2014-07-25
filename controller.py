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
    print request.form.get('first_name')
    print request.form.get('last_name')
    print request.form.get('email')
    print request.form.get('phone')
    print request.form.get('password')
    print request.form.get('role')

    # print request.files["photoimg"]

    # Create the user object to store our data
    user = User()
    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.email = request.form.get('email')
    user.phone = request.form.get('phone')
    user.password = request.form.get('password')
    user.role = request.form.get('role')

    print user.role

    existing = db_session.query(User).filter_by(email=user.email).first()
    if existing:
        flash("Email already in use", "error")
        return redirect(url_for("user_login_get"))


    # Add the user object to the database
    db_session.add(user)

    # Save the user in the database
    db_session.commit()

    print "User id: " + user.id
    # session['user_id'] = user.id
    
    # # save photo with user id as filename (1.jpg)

    #Log in user


    # # Redirect user to landing page
    return redirect(url_for("traveler_view"))

### Logout
@app.route("/logout")
def logout():
    del session['user_id']
    return redirect(url_for("user_login_get"))

### Traveler view
@app.route("/traveler_view", methods=["GET"])
def traveler_view():
    return render_template("traveler_view.html")

@app.route("/traveler_view", methods=["POST"])
def traveler_view_post():

    trip = Trip()
    trip.traveler_id = request.form.get('traveler_id')
    trip.traveler_current_lat = request.form.get('latStart')
    trip.traveler_current_long = request.form.get('longStart')
    trip.traveler_destination_lat = request.form.get('latEnd')
    trip.traveler_destination_long = request.form.get('longStart')

    # Add the user object to the database
    db_session.add(trip)

    # Save the user in the database
    db_session.commit()

    # Confirm
    return redirect(url_for("traveler_view"))

### Guide view
@app.route("/guide_view", methods=["GET"])
def guide_view():
    return render_template("guide_view.html")

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