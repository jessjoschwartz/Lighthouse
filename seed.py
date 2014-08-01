import model
import csv
import sqlalchemy.exc
import datetime
import re

def load_users(session):
    with open("seed_data/u.user") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            id, email, phone, first_name, last_name, password, role = row
            id = int(id)
            role = int(role)
            u = model.User(id=id, email=None, phone=None, password=None, first_name=first_name, last_name=last_name, role=role)
            session.add(u)
        try:
            session.commit()
        except sqlalchemy.exc.IntegrityError, e:
            session.rollback()

def load_trips(session):
    with open("seed_data/u.user") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            id, traveler_id, guide_id, traveler_current_lat, traveler_current_long, traveler_destination_lat, traveler_destination_long = row
            id = int(id)
            u = model.User(id=id, traveler_id=traveler_id, guide_id=guide_id, traveler_current_lat=traveler_current_lat, traveler_current_long=traveler_current_long, traveler_destination_lat=traveler_destination_lat, traveler_destination_long=traveler_destination_long)
            session.add(u)
        try:
            session.commit()
        except sqlalchemy.exc.IntegrityError, e:
            session.rollback()

def load_statuses(session):
    with open("seed_data/u.user") as f:
        reader = csv.reader(f, delimiter="|")
        for row in reader:
            id, trip_id, datetime_accepted, datetime_commenced, datetime_completed = row
            id = int(id)
            role = int(role)
            u = model.User(id=id, email=None, phone=None, password=None, first_name=first_name, last_name=last_name, role=role)
            session.add(u)
        try:
            session.commit()
        except sqlalchemy.exc.IntegrityError, e:
            session.rollback()

def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    load_trips(session)
    load_statuses(session)

if __name__ == "__main__":
    s = model.session
    main(s)