from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Date
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
    first_name = Column(String(64), nullable=True) 
    last_name = Column(String(64), nullable=True) 
    # photo = Column(String(64), nullable=True) make it with blob
    password = Column(String(64), nullable=True)  
    traveler = Column(Integer, nullable = True)
    guide = Column(Integer, nullable = True)
    both = Column(Integer, nullable = True)

### End class declarations

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
    u1 = session.query(User).get(1)
    main()