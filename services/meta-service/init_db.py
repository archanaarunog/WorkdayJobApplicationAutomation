"""
Initialize database with updated schema.
This will create all tables based on the current models.

Usage:
    python init_db.py
"""

from src.config.database import Base, engine
from src.models import job, user, application

print("=" * 60)
print("Database Initialization")
print("=" * 60)

# Create all tables
Base.metadata.create_all(bind=engine)

print("✅ Database tables created successfully!")
print("=" * 60)
