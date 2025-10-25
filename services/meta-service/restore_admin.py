#!/usr/bin/env python3
"""
Restore admin user and test data after Phase 6 migration.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.database import SQLALCHEMY_DATABASE_URL
from src.models import User, Company, Job
from src.services.auth import hash_password

def main():
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Get default company
        default_company = db.query(Company).filter(Company.slug == "default").first()
        print(f"🏢 Default company ID: {default_company.id}")
        
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.email == "archanaarunog@gmail.com").first()
        if existing_admin:
            print("✅ Admin user already exists!")
            return
        
        # Create admin user
        hashed_password = hash_password("password123")
        admin_user = User(
            email="archanaarunog@gmail.com",
            password_hash=hashed_password,
            first_name="Archana",
            last_name="Arunachalam",
            phone="+1234567890",
            is_admin=True,
            company_id=default_company.id
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        # Set as company admin
        default_company.admin_user_id = admin_user.id
        db.commit()
        
        print("✅ Admin user created successfully!")
        print(f"   Email: {admin_user.email}")
        print(f"   Password: password123")
        print(f"   ID: {admin_user.id}")
        print(f"   Company: {default_company.name}")
        
        # Create some sample jobs
        sample_jobs = [
            Job(
                title="Senior Software Engineer",
                company="Default Company",
                location="Remote",
                description="Build amazing software products",
                requirements="5+ years Python experience",
                job_type="Full-time",
                salary_min=80000,
                salary_max=120000,
                company_id=default_company.id
            ),
            Job(
                title="Product Manager", 
                company="Default Company",
                location="San Francisco, CA",
                description="Lead product development initiatives",
                requirements="3+ years PM experience",
                job_type="Full-time",
                salary_min=90000,
                salary_max=140000,
                company_id=default_company.id
            )
        ]
        
        for job in sample_jobs:
            db.add(job)
        
        db.commit()
        print(f"✅ Created {len(sample_jobs)} sample jobs")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()