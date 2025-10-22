"""
Seed script to populate database with 25 sample jobs.
Run this script to add sample job listings to the database.

Usage:
    python seed_jobs.py
"""

from src.config.database import SessionLocal, engine
from src.models import job, user, application  # Import all models to avoid circular dependency
import random

# Sample data pools
COMPANIES = [
    "Meta", "Google", "Amazon", "Microsoft", "Apple", "Netflix", "Tesla",
    "Spotify", "Adobe", "Salesforce", "Oracle", "IBM", "Intel", "NVIDIA",
    "Airbnb", "Uber", "Lyft", "Twitter", "LinkedIn", "Dropbox"
]

JOB_TITLES = [
    "Software Engineer",
    "Senior Software Engineer",
    "Full Stack Developer",
    "Backend Developer",
    "Frontend Developer",
    "DevOps Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
    "Product Manager",
    "UX/UI Designer",
    "Cloud Architect",
    "Security Engineer",
    "Mobile Developer (iOS)",
    "Mobile Developer (Android)",
    "QA Engineer",
    "Site Reliability Engineer",
    "Data Engineer",
    "Business Analyst",
    "Technical Lead",
    "Engineering Manager"
]

LOCATIONS = [
    "Remote", "San Francisco, CA", "New York, NY", "Seattle, WA",
    "Austin, TX", "Boston, MA", "Los Angeles, CA", "Chicago, IL",
    "Denver, CO", "Portland, OR", "Miami, FL", "Atlanta, GA"
]

JOB_TYPES = ["Full-time", "Part-time", "Contract", "Internship"]

EXPERIENCES = [
    "0-2 years (Entry Level)",
    "2-5 years (Mid Level)",
    "5-10 years (Senior)",
    "10+ years (Lead/Principal)"
]

DESCRIPTIONS = [
    "We are seeking a talented professional to join our dynamic team. You will work on cutting-edge technologies and contribute to innovative solutions that impact millions of users worldwide.",
    "Join our team and help build the next generation of products. You'll collaborate with cross-functional teams to design, develop, and deploy scalable solutions.",
    "We're looking for a passionate individual to drive technical excellence. You will be responsible for architecting solutions, mentoring team members, and delivering high-quality software.",
    "Exciting opportunity to work on mission-critical projects. You'll leverage modern technologies and best practices to solve complex business challenges.",
    "Be part of a fast-growing company where you can make a real impact. You'll work in an agile environment with talented engineers and contribute to key initiatives.",
    "We need a creative problem-solver who thrives in collaborative environments. You'll design and implement features that enhance user experience and drive business growth.",
    "Join us in shaping the future of technology. You'll work on innovative projects, learn from industry experts, and grow your career in a supportive culture.",
    "Looking for someone who is passionate about technology and innovation. You'll be empowered to take ownership, experiment with new ideas, and drive meaningful change.",
    "Help us build world-class products that delight customers. You'll work with modern tools and frameworks while collaborating with talented peers.",
    "We value technical excellence and teamwork. You'll contribute to scalable systems, participate in code reviews, and continuously improve our engineering practices."
]


def create_sample_jobs():
    """Create 25 sample jobs in the database."""
    db = SessionLocal()
    
    try:
        # Check if jobs already exist
        existing_count = db.query(job.Job).count()
        if existing_count >= 25:
            print(f"✓ Database already has {existing_count} jobs. Skipping seed.")
            return
        
        print("Creating 25 sample jobs...")
        
        jobs_to_create = []
        for i in range(25):
            salary_base = random.randint(50, 200) * 1000  # $50k - $200k
            new_job = job.Job(
                title=JOB_TITLES[i % len(JOB_TITLES)],
                description=random.choice(DESCRIPTIONS),
                location=random.choice(LOCATIONS),
                job_type=random.choice(JOB_TYPES),
                salary_min=salary_base,
                salary_max=salary_base + random.randint(20, 50) * 1000,  # +$20k-$50k range
                experience_level=random.choice(EXPERIENCES),
                company=COMPANIES[i % len(COMPANIES)]
            )
            jobs_to_create.append(new_job)
        
        # Add all jobs to database
        db.add_all(jobs_to_create)
        db.commit()
        
        print(f"✅ Successfully created 25 sample jobs!")
        print(f"📊 Total jobs in database: {db.query(job.Job).count()}")
        
        # Show first 5 jobs as sample
        print("\n📋 Sample jobs created:")
        for j in jobs_to_create[:5]:
            print(f"  - {j.title} at {j.company} ({j.location}) - ${j.salary_min:,} - ${j.salary_max:,}")
        print(f"  ... and {len(jobs_to_create) - 5} more jobs")
        
    except Exception as e:
        print(f"❌ Error creating jobs: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 60)
    print("Job Database Seeder")
    print("=" * 60)
    create_sample_jobs()
    print("=" * 60)
