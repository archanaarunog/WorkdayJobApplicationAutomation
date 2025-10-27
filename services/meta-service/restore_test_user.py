#!/usr/bin/env python3
"""
Script to restore test user credentials to database
"""

import sys
sys.path.insert(0, '/Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service')

from src.config.database import engine, Base, SessionLocal
from src.models.user import User
from src.models.company import Company
from src.services.auth import hash_password

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

try:
    # Check if default company exists
    default_company = db.query(Company).filter(Company.slug == "default").first()
    if not default_company:
        print("Creating default company...")
        default_company = Company(
            name="Meta",
            slug="default",
            description="Default company for testing"
        )
        db.add(default_company)
        db.commit()
        db.refresh(default_company)
        print(f"✅ Default company created (ID: {default_company.id})")
    else:
        print(f"✅ Default company exists (ID: {default_company.id})")

    # Check if test user exists
    test_user = db.query(User).filter(User.email == "alice5678@example.com").first()
    
    if test_user:
        print(f"✅ Test user already exists: {test_user.email}")
        print(f"   User ID: {test_user.id}")
        print(f"   Company ID: {test_user.company_id}")
        print(f"   Created at: {test_user.created_at}")
    else:
        print("Creating test user...")
        test_user = User(
            email="alice5678@example.com",
            password_hash=hash_password("SecurePass@123"),
            first_name="Aliceia",
            last_name="Johnsons",
            phone="8056095517",
            company_id=default_company.id
        )
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        print(f"✅ Test user created")
        print(f"   Email: {test_user.email}")
        print(f"   User ID: {test_user.id}")
        print(f"   Company ID: {test_user.company_id}")
        print(f"   Created at: {test_user.created_at}")

    print("\n✨ Database restored successfully!")
    print("\nYou can now login with:")
    print("  Email:    alice5678@example.com")
    print("  Password: SecurePass@123")

finally:
    db.close()
