"""
User model for Meta Portal.

This file defines what a User looks like in our database.
Think of it as a blueprint for a user table.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from ..config.database import Base

class User(Base):
    """
    User table definition.
    Each attribute becomes a column in the database.
    """
    __tablename__ = "users"  # This will be the table name in the database

    # Primary key - unique identifier for each user
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # User information - all required fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # We never store plain passwords!
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)  # Required field as per user story
    
    # Timestamps - automatically track when records are created/updated
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Status tracking
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        """
        This method defines how the User object looks when printed.
        Useful for debugging.
        """
        return f"<User(id={self.id}, email='{self.email}', name='{self.first_name} {self.last_name}')>"
