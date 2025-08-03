"""
Database configuration for Meta Portal.

This file sets up the connection to our SQLite database.
SQLite is a simple database that stores data in a single file.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get the path to our project root (5 levels up to get to WorkdayJobApplicationAutomation/)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
database_path = os.path.join(project_root, "databases", "meta.db")

# Create the database URL - SQLite uses file:// format
SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_path}"

# Create the database engine
# check_same_thread=False allows multiple threads to use the same connection 
# this being able to have multiple users access the database at the same time
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Create a session factory
# Sessions are how we talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our database models
# All our database tables will inherit from this
Base = declarative_base()

def get_db():
    """
    This function creates a database session for each request.
    It's like opening a conversation with the database.
    """
    db = SessionLocal()
    try:
        yield db  # Give the session to whoever needs it
    finally:
        db.close()  # Always close the session when done
