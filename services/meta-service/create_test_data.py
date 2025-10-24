"""
Script to add test data for admin dashboard testing.
This will create sample applications so the admin can see real data.
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

def create_test_data():
    """Create sample applications for admin dashboard testing."""
    
    with Session(engine) as db:
        
        # Check if we already have test data
        existing_apps = db.query(Application).count()
        if existing_apps > 0:
            print(f"✅ Found {existing_apps} existing applications")
            response = input("Do you want to add more test data? (y/n): ")
            if response.lower() != 'y':
                return
        
        # Get existing jobs and users
        jobs = db.query(Job).all()
        users = db.query(User).filter(User.is_admin == False).all()
        
        if not jobs:
            print("❌ No jobs found. Please run seed_jobs.py first to create sample jobs.")
            return
            
        if not users:
            print("❌ No users found. Please register some users first.")
            return
            
        print(f"📊 Found {len(jobs)} jobs and {len(users)} users")
        
        # Create sample applications
        statuses = ['submitted', 'in_review', 'interview', 'accepted', 'rejected']
        cover_letters = [
            "I am very interested in this position and believe my skills align perfectly with your requirements.",
            "With my extensive background in software development, I am excited to contribute to your team.",
            "This role represents exactly the kind of opportunity I have been seeking to advance my career.",
            "I am passionate about technology and would love to bring my expertise to your organization.",
            "My experience in the industry has prepared me well for this challenging and rewarding position."
        ]
        
        applications_created = 0
        
        # Create applications for each user
        for user in users:
            # Each user applies to 1-3 random jobs
            num_applications = random.randint(1, min(3, len(jobs)))
            selected_jobs = random.sample(jobs, num_applications)
            
            for job in selected_jobs:
                # Check if application already exists
                existing = db.query(Application).filter(
                    Application.user_id == user.id,
                    Application.job_id == job.id
                ).first()
                
                if existing:
                    continue  # Skip if already applied
                
                # Create application
                application = Application(
                    user_id=user.id,
                    job_id=job.id,
                    cover_letter=random.choice(cover_letters),
                    status=random.choice(statuses),
                    applied_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
                )
                
                db.add(application)
                applications_created += 1
        
        # Commit all changes
        db.commit()
        
        # Show summary
        total_applications = db.query(Application).count()
        status_counts = {}
        for status in statuses:
            count = db.query(Application).filter(Application.status == status).count()
            status_counts[status] = count
        
        print(f"\n✅ Test data creation complete!")
        print(f"   📋 Total Applications: {total_applications}")
        print(f"   🆕 New Applications: {applications_created}")
        print(f"\n📊 Status Breakdown:")
        for status, count in status_counts.items():
            print(f"   {status.replace('_', ' ').title()}: {count}")
        
        print(f"\n🎯 Now test the admin dashboard:")
        print(f"   1. Go to: http://localhost:8081/admin-dashboard.html")
        print(f"   2. Login with your admin account")
        print(f"   3. Verify statistics show correct numbers")
        print(f"   4. Test status filters and updates")

if __name__ == "__main__":
    create_test_data()