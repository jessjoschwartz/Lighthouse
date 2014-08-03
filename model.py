from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Date, Float
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref

import os

db_uri = os.environ.get("DATABASE_URL", "sqlite:///users.db")
    
engine = create_engine(db_uri, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property

### Class declarations go here

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True, unique=True)
    phone = Column(String(64), nullable=False)
    first_name = Column(String(64), nullable=False)  
    last_name = Column(String(64), nullable=False) 
    password = Column(String(64), nullable=False)  
    role = Column(Integer, nullable = False)

class Trip(Base):
    __tablename__ = "trips"
    
    id = Column(Integer, primary_key = True)
    traveler_id = Column(Integer, ForeignKey('users.id'))
    guide_id = Column(Integer, ForeignKey('users.id'))
    traveler_current_lat = Column(Float(20), nullable=False)
    traveler_current_long = Column(Float(20), nullable=False)
    traveler_destination_lat = Column(Float(20), nullable=False)
    traveler_destination_long = Column(Float(20), nullable=False)
    traveler_current_address = Column(String(64), nullable=False)
    traveler_destination_address = Column(String(64), nullable=False)
    # guide_current_location_lat = Column(Float(20), nullable=True)
    # guide_current_location_long = Column(Float(20), nullable=True)

    traveler = relationship("User", foreign_keys=[traveler_id]) 
    guide = relationship("User", foreign_keys=[guide_id]) 

    # traveler = relationship("User", backref="trips") 
    # guide = relationship("User" , backref="trips") 

    # traveler = relationship("User", backref=backref("trips", order_by=id))
    # guide = relationship("User", backref=backref("trips", order_by=id))

class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key = True)
    trip_id = Column(Integer, ForeignKey('trips.id'))
    datetime_accepted = Column(DateTime, nullable=True)
    datetime_commenced = Column(DateTime, nullable=True)
    datetime_completed = Column(DateTime, nullable=True)

    trip = relationship("Trip", backref=backref("statuses"))

### End class declarations

class Trips(object):
    pass

def get_trips():
    all_users = session.query(User).all()
    all_trips = session.query(Trip).all()
    for t in all_trips:
        print t.traveler

    return all_trips

def get_trip(trip_id):
    return session.query(Trip).get(trip_id)

def get_status_for_trip(trip_id):
    return session.query(Status).filter_by(trip_id = trip_id).first()

def create_db():
    Base.metadata.create_all(engine)

def connect(db_uri="sqlite:///users.db"):
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
    # u1 = session.query(User).get()
    main()