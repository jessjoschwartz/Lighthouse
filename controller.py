from flask import Flask, session, request, flash, redirect, url_for
from model import session as db_session, User
import model
import os

app = Flask(__name__)
SECRET_KEY = "fish"
app.config.from_object(__name__)

@app.route("/login", methods=["POST"])
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

@app.route("/register/1", methods=["POST"])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']
    existing = db_session.query(User).filter_by(email=email).first()
    if existing:
        flash("Email already in use", "error")
        return redirect(url_for("login"))

    u = User(email=email, password=password, first_name=first_name, last_name=last_name, phone=phone)
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    session['user_id'] = u.id 
    return redirect(url_for("display_search"))

@app.route("/logout")
def logout():
    del session['user_id']
    return redirect(url_for("login"))

if __name__ == "__main__":
    db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
    if not db_uri:
        db_uri = "sqlite:///all_users.db"
    model.connect(db_uri)
    app.run(debug=True, port=int(os.environ.get("PORT", 5000)), host="0.0.0.0")