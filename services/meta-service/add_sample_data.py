#!/usr/bin/env python3
"""
Add sample companies and data for testing Phase 6
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
        
        # Add some jobs to default company
        sample_jobs = [
            Job(
                title="Senior Software Engineer",
                location="Remote",
                description="Build amazing software products with cutting-edge technology",
                requirements="5+ years Python/JavaScript experience, API development",
                job_type="Full-time",
                salary_min=90000,
                salary_max=130000,
                company_id=default_company.id
            ),
            Job(
                title="Product Manager", 
                location="San Francisco, CA",
                description="Lead product development and strategy for our core platform",
                requirements="3+ years PM experience, Technical background preferred",
                job_type="Full-time",
                salary_min=100000,
                salary_max=150000,
                company_id=default_company.id
            ),
            Job(
                title="UI/UX Designer",
                location="New York, NY",
                description="Design beautiful and intuitive user experiences",
                requirements="Portfolio required, Figma/Sketch expertise",
                job_type="Full-time",
                salary_min=70000,
                salary_max=110000,
                company_id=default_company.id
            )
        ]
        
        for job in sample_jobs:
            existing = db.query(Job).filter(Job.title == job.title).first()
            if not existing:
                db.add(job)
        
        db.commit()
        print("✅ Added sample jobs to Default Company")
        
        # Create a second test company
        test_company = db.query(Company).filter(Company.slug == "tech-corp").first()
        if not test_company:
            test_company = Company(
                name="Tech Corp Inc",
                slug="tech-corp", 
                domain="techcorp.com",
                description="Leading technology solutions provider",
                industry="Technology",
                website="https://techcorp.com",
                headquarters="Seattle, WA",
                size="Medium (50-200 employees)",
                is_active=True,
                settings={
                    'job_posting_approval_required': True,
                    'allow_external_applications': True,
                    'email_notifications': True,
                    'branding_color': '#28a745',
                    'logo_url': None,
                    'custom_application_fields': ['Portfolio URL', 'GitHub Profile']
                }
            )
            db.add(test_company)
            db.commit()
            db.refresh(test_company)
            print(f"✅ Created test company: {test_company.name}")
            
            # Add jobs for test company
            tech_jobs = [
                Job(
                    title="DevOps Engineer",
                    location="Seattle, WA", 
                    description="Manage cloud infrastructure and deployment pipelines",
                    requirements="AWS/Azure experience, Docker, Kubernetes",
                    job_type="Full-time",
                    salary_min=95000,
                    salary_max=140000,
                    company_id=test_company.id
                ),
                Job(
                    title="Data Scientist",
                    location="Remote",
                    description="Extract insights from large datasets using ML/AI",
                    requirements="Python, SQL, Machine Learning, Statistics",
                    job_type="Full-time", 
                    salary_min=110000,
                    salary_max=160000,
                    company_id=test_company.id
                )
            ]
            
            for job in tech_jobs:
                db.add(job)
            db.commit()
            print(f"✅ Added jobs for {test_company.name}")
        
        # Summary
        total_companies = db.query(Company).count()
        total_jobs = db.query(Job).count()
        total_users = db.query(User).count()
        
        print(f"\n📊 Database Summary:")
        print(f"   Companies: {total_companies}")
        print(f"   Jobs: {total_jobs}")
        print(f"   Users: {total_users}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()