"""
Complete Setup Script - Creates Companies, Jobs, Users, and Applications
Runs all setup tasks in the correct order
"""

import sys
import os
from datetime import datetime, timedelta
import random

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from src.config.database import engine, SessionLocal
from src.models.user import User
from src.models.company import Company
from src.models.job import Job
from src.models.application import Application
from src.services.auth import hash_password

# Sample data
COMPANY_DATA = [
    {"name": "Meta", "slug": "meta", "domain": "meta.com", "industry": "Technology", "size": "Large (201-1000)", "headquarters": "Menlo Park, CA"},
    {"name": "Google", "slug": "google", "domain": "google.com", "industry": "Technology", "size": "Enterprise (1000+)", "headquarters": "Mountain View, CA"},
    {"name": "Amazon", "slug": "amazon", "domain": "amazon.com", "industry": "Technology", "size": "Enterprise (1000+)", "headquarters": "Seattle, WA"},
    {"name": "Microsoft", "slug": "microsoft", "domain": "microsoft.com", "industry": "Technology", "size": "Enterprise (1000+)", "headquarters": "Redmond, WA"},
    {"name": "Apple", "slug": "apple", "domain": "apple.com", "industry": "Technology", "size": "Enterprise (1000+)", "headquarters": "Cupertino, CA"},
    {"name": "Netflix", "slug": "netflix", "domain": "netflix.com", "industry": "Entertainment", "size": "Large (201-1000)", "headquarters": "Los Gatos, CA"},
    {"name": "Tesla", "slug": "tesla", "domain": "tesla.com", "industry": "Automotive", "size": "Large (201-1000)", "headquarters": "Palo Alto, CA"},
    {"name": "Spotify", "slug": "spotify", "domain": "spotify.com", "industry": "Music", "size": "Medium (51-200)", "headquarters": "Stockholm, Sweden"},
    {"name": "Adobe", "slug": "adobe", "domain": "adobe.com", "industry": "Software", "size": "Large (201-1000)", "headquarters": "San Jose, CA"},
    {"name": "Salesforce", "slug": "salesforce", "domain": "salesforce.com", "industry": "Software", "size": "Large (201-1000)", "headquarters": "San Francisco, CA"},
    {"name": "Oracle", "slug": "oracle", "domain": "oracle.com", "industry": "Software", "size": "Enterprise (1000+)", "headquarters": "Austin, TX"},
    {"name": "IBM", "slug": "ibm", "domain": "ibm.com", "industry": "Technology", "size": "Enterprise (1000+)", "headquarters": "Armonk, NY"},
    {"name": "Intel", "slug": "intel", "domain": "intel.com", "industry": "Semiconductor", "size": "Large (201-1000)", "headquarters": "Santa Clara, CA"},
    {"name": "NVIDIA", "slug": "nvidia", "domain": "nvidia.com", "industry": "Semiconductor", "size": "Large (201-1000)", "headquarters": "Santa Clara, CA"},
    {"name": "Airbnb", "slug": "airbnb", "domain": "airbnb.com", "industry": "Travel", "size": "Medium (51-200)", "headquarters": "San Francisco, CA"},
    {"name": "Uber", "slug": "uber", "domain": "uber.com", "industry": "Transportation", "size": "Large (201-1000)", "headquarters": "San Francisco, CA"},
    {"name": "Lyft", "slug": "lyft", "domain": "lyft.com", "industry": "Transportation", "size": "Medium (51-200)", "headquarters": "San Francisco, CA"},
    {"name": "Twitter", "slug": "twitter", "domain": "twitter.com", "industry": "Social Media", "size": "Medium (51-200)", "headquarters": "San Francisco, CA"},
    {"name": "LinkedIn", "slug": "linkedin", "domain": "linkedin.com", "industry": "Social Media", "size": "Large (201-1000)", "headquarters": "Sunnyvale, CA"},
    {"name": "Dropbox", "slug": "dropbox", "domain": "dropbox.com", "industry": "Cloud Storage", "size": "Medium (51-200)", "headquarters": "San Francisco, CA"},
    {"name": "Slack", "slug": "slack", "domain": "slack.com", "industry": "Communication", "size": "Medium (51-200)", "headquarters": "San Francisco, CA"},
    {"name": "Stripe", "slug": "stripe", "domain": "stripe.com", "industry": "Fintech", "size": "Medium (51-200)", "headquarters": "San Francisco, CA"},
    {"name": "Pinterest", "slug": "pinterest", "domain": "pinterest.com", "industry": "Social Media", "size": "Medium (51-200)", "headquarters": "San Francisco, CA"},
    {"name": "Snap", "slug": "snap", "domain": "snap.com", "industry": "Social Media", "size": "Medium (51-200)", "headquarters": "Santa Monica, CA"},
    {"name": "Zoom", "slug": "zoom", "domain": "zoom.us", "industry": "Communication", "size": "Medium (51-200)", "headquarters": "San Jose, CA"},
]

JOB_TITLES = [
    "Software Engineer", "Senior Software Engineer", "Full Stack Developer",
    "Backend Developer", "Frontend Developer", "DevOps Engineer",
    "Data Scientist", "Machine Learning Engineer", "Product Manager",
    "UX/UI Designer", "Cloud Architect", "Security Engineer",
    "Mobile Developer (iOS)", "Mobile Developer (Android)", "QA Engineer",
    "Site Reliability Engineer", "Data Engineer", "Business Analyst",
    "Technical Lead", "Engineering Manager"
]

LOCATIONS = [
    "Remote", "San Francisco, CA", "New York, NY", "Seattle, WA",
    "Austin, TX", "Boston, MA", "Los Angeles, CA", "Chicago, IL",
    "Denver, CO", "Portland, OR", "Miami, FL", "Atlanta, GA"
]

JOB_TYPES = ["Full-time", "Part-time", "Contract", "Internship"]
EXPERIENCES = ["0-2 years (Entry Level)", "2-5 years (Mid Level)", "5-10 years (Senior)", "10+ years (Lead/Principal)"]

DESCRIPTIONS = [
    "We are seeking a talented professional to join our dynamic team. You will work on cutting-edge technologies and contribute to innovative solutions that impact millions of users worldwide.",
    "Join our team and help build the next generation of products. You'll collaborate with cross-functional teams to design, develop, and deploy scalable solutions.",
    "We're looking for a passionate individual to drive technical excellence. You will be responsible for architecting solutions, mentoring team members, and delivering high-quality software.",
    "Exciting opportunity to work on mission-critical projects. You'll leverage modern technologies and best practices to solve complex business challenges.",
    "Be part of a fast-growing company where you can make a real impact. You'll work in an agile environment with talented engineers and contribute to key initiatives.",
]

USER_DATA = [
    {"email": "john.doe@gmail.com", "password": "password123", "first_name": "John", "last_name": "Doe", "phone": "+1234567890"},
    {"email": "jane.smith@gmail.com", "password": "password123", "first_name": "Jane", "last_name": "Smith", "phone": "+1234567891"},
    {"email": "mike.johnson@gmail.com", "password": "password123", "first_name": "Mike", "last_name": "Johnson", "phone": "+1234567892"},
    {"email": "sarah.wilson@gmail.com", "password": "password123", "first_name": "Sarah", "last_name": "Wilson", "phone": "+1234567893"},
    {"email": "alex.brown@gmail.com", "password": "password123", "first_name": "Alex", "last_name": "Brown", "phone": "+1234567894"},
    {"email": "emily.davis@gmail.com", "password": "password123", "first_name": "Emily", "last_name": "Davis", "phone": "+1234567895"},
    {"email": "david.miller@gmail.com", "password": "password123", "first_name": "David", "last_name": "Miller", "phone": "+1234567896"},
    {"email": "sophia.anderson@gmail.com", "password": "password123", "first_name": "Sophia", "last_name": "Anderson", "phone": "+1234567897"},
    {"email": "christopher.taylor@gmail.com", "password": "password123", "first_name": "Christopher", "last_name": "Taylor", "phone": "+1234567898"},
    {"email": "olivia.thomas@gmail.com", "password": "password123", "first_name": "Olivia", "last_name": "Thomas", "phone": "+1234567899"},
]

COVER_LETTERS = [
    "I am very interested in this position and believe my skills align perfectly with your requirements.",
    "This role represents exactly the kind of opportunity I have been seeking to advance my career.",
    "I am excited about the possibility of joining your organization.",
    "Your company's mission and values align perfectly with my career goals.",
    "With my proven track record, I am well-positioned to excel in this role.",
]


def create_companies(db: Session):
    """Create 25 sample companies."""
    print("\n👥 Creating 25 companies...")
    created = 0
    
    for company_data in COMPANY_DATA:
        existing = db.query(Company).filter(Company.slug == company_data["slug"]).first()
        if existing:
            print(f"   ✓ {company_data['name']} already exists")
            continue
        
        company = Company(
            name=company_data["name"],
            slug=company_data["slug"],
            domain=company_data["domain"],
            industry=company_data["industry"],
            size=company_data["size"],
            headquarters=company_data["headquarters"],
            description=f"{company_data['name']} - {company_data['industry']} Company",
            website=f"https://{company_data['domain']}",
            is_active=True
        )
        db.add(company)
        created += 1
        print(f"   ✅ Created: {company_data['name']}")
    
    db.commit()
    return created


def create_jobs(db: Session):
    """Create sample jobs for each company."""
    print("\n💼 Creating jobs for each company...")
    companies = db.query(Company).all()
    jobs_created = 0
    
    for company_obj in companies:
        # 2-4 jobs per company
        num_jobs = random.randint(2, 4)
        for _ in range(num_jobs):
            salary_base = random.randint(50, 200) * 1000
            job_obj = Job()
            job_obj.title = random.choice(JOB_TITLES)
            job_obj.description = random.choice(DESCRIPTIONS)
            job_obj.location = random.choice(LOCATIONS)
            job_obj.job_type = random.choice(JOB_TYPES)
            job_obj.salary_min = salary_base
            job_obj.salary_max = salary_base + random.randint(20, 50) * 1000
            job_obj.experience_level = random.choice(EXPERIENCES)
            job_obj.department = "Engineering"
            job_obj.company_id = company_obj.id
            job_obj.is_active = True
            db.add(job_obj)
            jobs_created += 1
    
    db.commit()
    print(f"   ✅ Created {jobs_created} jobs across {len(companies)} companies")
    return jobs_created


def create_users(db: Session):
    """Create sample users."""
    print("\n👤 Creating sample users...")
    created = 0
    
    for user_data in USER_DATA:
        existing = db.query(User).filter(User.email == user_data["email"]).first()
        if existing:
            print(f"   ✓ {user_data['email']} already exists")
            continue
        
        hashed_password = hash_password(user_data["password"])
        user = User(
            email=user_data["email"],
            password_hash=hashed_password,
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone=user_data["phone"],
            is_admin=False
        )
        db.add(user)
        created += 1
        print(f"   ✅ Created: {user_data['email']}")
    
    db.commit()
    return created


def create_applications(db: Session):
    """Create sample applications."""
    print("\n📋 Creating sample applications...")
    
    users = db.query(User).filter(User.is_admin == False).all()
    jobs = db.query(Job).all()
    
    statuses = ['submitted', 'in_review', 'interview', 'accepted', 'rejected']
    status_weights = [0.3, 0.25, 0.2, 0.15, 0.1]
    
    apps_created = 0
    for user in users:
        num_applications = random.randint(2, min(4, len(jobs)))
        selected_jobs = random.sample(jobs, num_applications)
        
        for job in selected_jobs:
            existing = db.query(Application).filter(
                Application.user_id == user.id,
                Application.job_id == job.id
            ).first()
            
            if existing:
                continue
            
            status = random.choices(statuses, weights=status_weights)[0]
            application = Application(
                user_id=user.id,
                job_id=job.id,
                company_id=job.company_id,
                cover_letter=random.choice(COVER_LETTERS),
                status=status,
                applied_at=datetime.utcnow() - timedelta(days=random.randint(1, 30))
            )
            db.add(application)
            apps_created += 1
    
    db.commit()
    print(f"   ✅ Created {apps_created} applications")
    return apps_created


def main():
    """Run complete setup."""
    print("\n" + "="*70)
    print("🚀 COMPLETE SYSTEM SETUP - COMPANIES, JOBS, USERS & APPLICATIONS")
    print("="*70)
    
    db = SessionLocal()
    
    try:
        # Step 1: Create companies
        companies_created = create_companies(db)
        
        # Step 2: Create jobs
        jobs_created = create_jobs(db)
        
        # Step 3: Create users
        users_created = create_users(db)
        
        # Step 4: Create applications
        apps_created = create_applications(db)
        
        # Step 5: Statistics
        total_companies = db.query(Company).count()
        total_jobs = db.query(Job).count()
        total_users = db.query(User).filter(User.is_admin == False).count()
        total_applications = db.query(Application).count()
        
        print("\n" + "="*70)
        print("✅ SETUP COMPLETE!")
        print("="*70)
        print(f"\n📊 Summary:")
        print(f"   Companies: {total_companies}")
        print(f"   Jobs: {total_jobs}")
        print(f"   Users: {total_users}")
        print(f"   Applications: {total_applications}")
        
        # Status breakdown
        print(f"\n📋 Application Status Breakdown:")
        statuses = ['submitted', 'in_review', 'interview', 'accepted', 'rejected']
        for status in statuses:
            count = db.query(Application).filter(Application.status == status).count()
            print(f"   {status.replace('_', ' ').title()}: {count}")
        
        print(f"\n🎯 Next Steps:")
        print(f"   1. Backend running: ✓ (uvicorn on port 8000)")
        print(f"   2. Frontend running: ✓ (HTTP server on port 8081)")
        print(f"   3. Visit: http://localhost:8081/admin-dashboard.html")
        print(f"   4. Login with admin credentials")
        print(f"   5. Test the admin dashboard with all the new data!")
        
        print(f"\n👤 Test Accounts Created:")
        for user_data in USER_DATA[:3]:
            print(f"   Email: {user_data['email']} | Password: {user_data['password']}")
        print(f"   ... and {len(USER_DATA) - 3} more accounts")
        
        print(f"\n🏢 Companies Created:")
        for company_data in COMPANY_DATA[:3]:
            print(f"   • {company_data['name']} ({company_data['industry']})")
        print(f"   ... and {len(COMPANY_DATA) - 3} more companies")
        
        print("\n" + "="*70)
        print("✨ System is ready for testing!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during setup: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


if __name__ == "__main__":
    main()
