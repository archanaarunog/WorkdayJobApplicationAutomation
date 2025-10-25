"""
User model for Meta Portal.

This file defines what a User looks like in our database.
Think of it as a blueprint for a user table.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from src.config.database import Base

class User(Base):
    """
    User table definition.
    Each attribute becomes a column in the database.
    """
    __tablename__ = "users"  # This will be the table name in the database

    # Primary key - unique identifier for each user
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Company association for multi-tenancy
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)
    
    # User information - all required fields
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # We never store plain passwords!
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)  # Required field as per user story
    
    # Optional profile fields
    bio = Column(String(500), nullable=True)  # Short bio/summary
    skills = Column(String(500), nullable=True)  # Comma-separated skills
    experience = Column(String(1000), nullable=True)  # Work experience summary
    education = Column(String(500), nullable=True)  # Education details
    linkedin_url = Column(String(255), nullable=True)  # LinkedIn profile
    github_url = Column(String(255), nullable=True)  # GitHub profile
    
    # Timestamps - automatically track when records are created/updated
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Status tracking
    is_active = Column(Boolean, default=True, nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)  # Admin role flag

    # Relationships
    # This allows you to do: user.applications to get a list of Application objects
    # back_populates must match the name used in Application model's relationship to User
    from sqlalchemy.orm import relationship
    applications = relationship("Application", back_populates="user", cascade="all, delete-orphan")
    
    # Company relationship for multi-tenancy
    company = relationship("Company", back_populates="users", foreign_keys=[company_id])

    # __repr__ is a special method that defines how this object appears when you print it or inspect it in the Python shell.
    # It is not called automatically every time; it is used when you do print(user), repr(user), or see the object in debugging tools.
    def __repr__(self):
        """
        This method defines how the User object looks when printed or inspected.
        Useful for debugging and logging.
        """
        return f"<User(id={self.id}, email='{self.email}', name='{self.first_name} {self.last_name}')>"


"""
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
)

"""