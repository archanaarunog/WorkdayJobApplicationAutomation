"""
Script to make a user an admin.
Run this to grant admin privileges to your account.

Usage:
    python make_admin.py your@email.com
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from src.config.database import engine
from src.models.user import User

def make_admin(email: str):
    """Make a user an admin by email."""
    with Session(engine) as db:
        user = db.query(User).filter(User.email == email).first()
        
        if not user:
            print(f"❌ User with email '{email}' not found")
            return False
        
        if user.is_admin:
            print(f"✅ User '{email}' is already an admin")
            return True
        
        user.is_admin = True
        db.commit()
        print(f"✅ User '{email}' is now an admin!")
        print(f"   Name: {user.first_name} {user.last_name}")
        print(f"   You can now access the admin dashboard at: http://localhost:8081/admin-dashboard.html")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python make_admin.py your@email.com")
        sys.exit(1)
    
    email = sys.argv[1]
    make_admin(email)
