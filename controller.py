from flask import Flask, session, request, flash, redirect, url_for, render_template
from model import session as db_session, User
import model
import os

app = Flask(__name__)
SECRET_KEY = "fish"
app.config.from_object(__name__)

### Login page
@app.route("/", methods=["GET"])
def display_start():
    return render_template("start.html")

@app.route("/", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']

    try:
        user = db_session.query(User).filter_by(email=email, password=password).one()
    except:
        flash("Invalid username or password", "error")
        return redirect(url_for("login"))

    session['user_id'] = user.id
    return redirect(url_for("display_search"))

### User login
@app.route("/login", methods=["GET"])
def user_login():
    return render_template("user_login.html")

### Registration page #1
@app.route("/register/1", methods=["GET"])
def display_register_1():
    return render_template("register_1.html")

### Registration page #2

@app.route("/register/2", methods=["GET"])
def register():
    return render_template("register_2.html")

@app.route("/register/2", methods=["POST"])
def display_register_2():
    print request.files["photoimg"]
    return render_template("register_2.html")

    existing = db_session.query(User).filter_by(email=email).first()
    if existing:
        flash("Email already in use", "error")
        return redirect(url_for("login"))

    # Create the user object to store our data
    user = User()
    user.first_name = request.form.get('first_name')
    user.last_name = request.form.get('last_name')
    user.email = request.form('email')
    user.phone = request.form('phone')
    user.password = request.form('password')

    # Add the user object to the database
    db_session.add(user)

    # Save the user in the database
    db_session.commit()

    # Redirect user to landing page
    return redirect(url_for("traveler_trip_request"))

### Logout
@app.route("/logout")
def logout():
    del session['user_id']
    return redirect(url_for("login"))

### End class declarations

def create_db():
    Base.metadata.create_all(engine)

def connect(db_uri="sqlite:///ratings.db"):
    global engine
    global session
    engine = create_engine(db_uri, echo=False) 
    session = scoped_session(sessionmaker(bind=engine,
                             autocommit = False,
                             autoflush = False))

def main():
    """In case we need this for something"""
    pass    

if __name__ == "__main__":
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if not db_uri:
        db_uri = "sqlite:///all_users.db"
    model.connect(db_uri)
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host="0.0.0.0")