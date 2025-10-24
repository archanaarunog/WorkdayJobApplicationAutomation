"""
Complete Test Data Setup
Creates users, jobs, and applications for full admin testing
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from src.config.database import engine
from src.models.user import User
from src.models.job import Job
from src.models.application import Application
from src.services.auth import hash_password

def create_sample_users(db: Session):
    """Create sample users for testing."""
    
    sample_users = [
        {
            "email": "john.doe@gmail.com",
            "password": "password123",
            "first_name": "John",
            "last_name": "Doe",
            "phone": "+1234567890"
        },
        {
            "email": "jane.smith@gmail.com", 
            "password": "password123",
            "first_name": "Jane",
            "last_name": "Smith",
            "phone": "+1234567891"
        },
        {
            "email": "mike.johnson@gmail.com",
            "password": "password123", 
            "first_name": "Mike",
            "last_name": "Johnson",
            "phone": "+1234567892"
        },
        {
            "email": "sarah.wilson@gmail.com",
            "password": "password123",
            "first_name": "Sarah", 
            "last_name": "Wilson",
            "phone": "+1234567893"
        },
        {
            "email": "alex.brown@gmail.com",
            "password": "password123",
            "first_name": "Alex",
            "last_name": "Brown", 
            "phone": "+1234567894"
        }
    ]
    
    created_users = []
    
    for user_data in sample_users:
        # Check if user already exists
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            print(f"   👤 User {user_data['email']} already exists")
            created_users.append(existing)
            continue
            
        # Hash password
        hashed_password = hash_password(user_data["password"])
        
        # Create user
        user = User(
            email=user_data["email"],
            password_hash=hashed_password,
            first_name=user_data["first_name"],
            last_name=user_data["last_name"], 
            phone=user_data["phone"],
            is_admin=False
        )
        
        db.add(user)
        created_users.append(user)
        print(f"   ✅ Created user: {user_data['email']}")
    
    db.commit()
    return created_users

def create_sample_applications(db: Session, users, jobs):
    """Create sample applications."""
    
    statuses = ['submitted', 'in_review', 'interview', 'accepted', 'rejected']
    cover_letters = [
        "I am very interested in this position and believe my skills align perfectly with your requirements. With my extensive experience in software development, I am confident I can contribute effectively to your team.",
        
        "This role represents exactly the kind of opportunity I have been seeking to advance my career. My background in technology and passion for innovation make me an ideal candidate for this position.",
        
        "I am excited about the possibility of joining your organization. My technical skills and experience in the industry have prepared me well for this challenging and rewarding role.",
        
        "Your company's mission and values align perfectly with my career goals. I would love to bring my expertise and enthusiasm to contribute to your team's continued success.",
        
        "With my proven track record in software development and strong problem-solving skills, I am well-positioned to excel in this role and make a meaningful impact on your projects."
    ]
    
    applications_created = 0
    
    for user in users:
        # Each user applies to 2-4 random jobs
        num_applications = random.randint(2, min(4, len(jobs)))
        selected_jobs = random.sample(jobs, num_applications)
        
        for job in selected_jobs:
            # Check if application already exists
            existing = db.query(Application).filter(
                Application.user_id == user.id,
                Application.job_id == job.id
            ).first()
            
            if existing:
                continue
            
            # Create application with realistic status distribution
            status_weights = [0.3, 0.25, 0.2, 0.15, 0.1]  # More submitted/in_review
            status = random.choices(statuses, weights=status_weights)[0]
            
            application = Application(
                user_id=user.id,
                job_id=job.id,
                cover_letter=random.choice(cover_letters),
                status=status,
                applied_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            
            db.add(application)
            applications_created += 1
            print(f"   📋 {user.first_name} applied to {job.title} at {job.company} ({status})")
    
    db.commit()
    return applications_created

def main():
    """Main setup function."""
    print("=" * 70)
    print("🚀 COMPLETE ADMIN DASHBOARD SETUP")
    print("=" * 70)
    
    with Session(engine) as db:
        
        # Step 1: Check existing data
        existing_users = db.query(User).filter(User.is_admin == False).count()
        existing_jobs = db.query(Job).count() 
        existing_apps = db.query(Application).count()
        
        print(f"\n📊 Current Data:")
        print(f"   Users: {existing_users}")
        print(f"   Jobs: {existing_jobs}")
        print(f"   Applications: {existing_apps}")
        
        # Step 2: Create jobs if needed
        if existing_jobs == 0:
            print(f"\n💼 Creating sample jobs...")
            os.system("python seed_jobs.py")
        else:
            print(f"\n✅ Jobs already exist ({existing_jobs} jobs)")
            
        # Step 3: Create sample users
        print(f"\n👥 Creating sample users...")
        users = create_sample_users(db)
        
        # Step 4: Get all jobs
        jobs = db.query(Job).all()
        print(f"\n💼 Found {len(jobs)} jobs")
        
        # Step 5: Create sample applications  
        print(f"\n📋 Creating sample applications...")
        apps_created = create_sample_applications(db, users, jobs)
        
        # Step 6: Final statistics
        total_users = db.query(User).filter(User.is_admin == False).count()
        total_applications = db.query(Application).count()
        
        print(f"\n" + "=" * 50)
        print(f"✅ SETUP COMPLETE!")
        print(f"=" * 50)
        print(f"👥 Total Users: {total_users}")
        print(f"💼 Total Jobs: {len(jobs)}")
        print(f"📋 Total Applications: {total_applications}")
        print(f"🆕 New Applications: {apps_created}")
        
        # Status breakdown
        statuses = ['submitted', 'in_review', 'interview', 'accepted', 'rejected']
        print(f"\n📊 Application Status Breakdown:")
        for status in statuses:
            count = db.query(Application).filter(Application.status == status).count()
            print(f"   {status.replace('_', ' ').title()}: {count}")
        
        print(f"\n🎯 Next Steps:")
        print(f"   1. Make sure backend is running: uvicorn src.main:app --reload")
        print(f"   2. Make sure frontend is running: python3 -m http.server 8081")
        print(f"   3. Go to: http://localhost:8081/admin-dashboard.html")
        print(f"   4. Login with your admin account")
        print(f"   5. Test all admin features!")
        
        print(f"\n📝 Test Accounts Created:")
        for user in users:
            print(f"   Email: {user.email} | Password: password123")

if __name__ == "__main__":
    main()