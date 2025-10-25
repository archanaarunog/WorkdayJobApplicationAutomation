"""
Database Migration Script for Multi-Company Architecture (Phase 6)

This script migrates the existing database to support multi-tenancy by:
1. Creating the companies table
2. Adding company_id columns to existing tables
3. Creating a default company for existing data
4. Setting up proper relationships

Run this script after backing up your database!
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from src.config.database import SQLALCHEMY_DATABASE_URL, Base
from src.models import User, Job, Application, Company
import sqlite3
from datetime import datetime

def backup_database():
    """Create a backup of the current database"""
    import shutil
    db_path = "databases/meta.db"
    backup_path = f"databases/meta_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    
    if os.path.exists(db_path):
        shutil.copy2(db_path, backup_path)
        print(f"✅ Database backed up to {backup_path}")
        return backup_path
    else:
        print("⚠️  No existing database found. Creating fresh database.")
        return None

def add_company_columns():
    """Add company_id columns to existing tables"""
    db_path = "databases/meta.db"
    
    if not os.path.exists(db_path):
        print("No existing database found. Will create new one.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Add company_id to users table
        cursor.execute("ALTER TABLE users ADD COLUMN company_id INTEGER")
        print("✅ Added company_id column to users table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ℹ️  company_id column already exists in users table")
        else:
            print(f"⚠️  Error adding company_id to users: {e}")
    
    try:
        # Add company_id to jobs table
        cursor.execute("ALTER TABLE jobs ADD COLUMN company_id INTEGER")
        print("✅ Added company_id column to jobs table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ℹ️  company_id column already exists in jobs table")
        else:
            print(f"⚠️  Error adding company_id to jobs: {e}")
    
    try:
        # Add company_id to applications table
        cursor.execute("ALTER TABLE applications ADD COLUMN company_id INTEGER")
        print("✅ Added company_id column to applications table")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ℹ️  company_id column already exists in applications table")
        else:
            print(f"⚠️  Error adding company_id to applications: {e}")
    
    conn.commit()
    conn.close()

def create_default_company_and_migrate_data():
    """Create default company and assign existing data to it"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    
    # Create all tables (including new companies table)
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created/updated")
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if default company already exists
        default_company = db.query(Company).filter(Company.slug == "default").first()
        
        if not default_company:
            # Create default company
            default_company = Company(
                name="Default Company",
                slug="default",
                domain=None,
                description="Default company for migrated data",
                industry="General",
                is_active=True,
                settings={
                    'job_posting_approval_required': False,
                    'allow_external_applications': True,
                    'email_notifications': True,
                    'branding_color': '#007bff',
                    'logo_url': None,
                    'custom_application_fields': []
                }
            )
            db.add(default_company)
            db.commit()
            db.refresh(default_company)
            print(f"✅ Created default company with ID: {default_company.id}")
        else:
            print(f"ℹ️  Default company already exists with ID: {default_company.id}")
        
        # Check if there are existing users, jobs, and applications to migrate
        total_users = db.query(User).count()
        total_jobs = db.query(Job).count()
        total_applications = db.query(Application).count()
        
        if total_users > 0 or total_jobs > 0 or total_applications > 0:
            # Migrate existing users
            users_without_company = db.query(User).filter(User.company_id.is_(None)).all()
            if users_without_company:
                for user in users_without_company:
                    user.company_id = default_company.id
                db.commit()
                print(f"✅ Migrated {len(users_without_company)} users to default company")
            
            # Migrate existing jobs
            jobs_without_company = db.query(Job).filter(Job.company_id.is_(None)).all()
            if jobs_without_company:
                for job in jobs_without_company:
                    job.company_id = default_company.id
                db.commit()
                print(f"✅ Migrated {len(jobs_without_company)} jobs to default company")
            
            # Migrate existing applications (set company_id based on job's company)
            applications_without_company = db.query(Application).filter(Application.company_id.is_(None)).all()
            if applications_without_company:
                for application in applications_without_company:
                    # Get the job for this application
                    job = db.query(Job).filter(Job.id == application.job_id).first()
                    if job and job.company_id:
                        application.company_id = job.company_id
                    else:
                        application.company_id = default_company.id
                db.commit()
                print(f"✅ Migrated {len(applications_without_company)} applications to companies")
        else:
            print("ℹ️  No existing data to migrate. Fresh database setup complete.")
        
        # Find first admin user and set as company admin (only if there are existing users)
        if total_users > 0:
            admin_user = db.query(User).filter(User.is_admin == True, User.company_id == default_company.id).first()
            if admin_user and not default_company.admin_user_id:
                default_company.admin_user_id = admin_user.id
                db.commit()
                print(f"✅ Set user {admin_user.email} as admin for default company")
        else:
            print("ℹ️  No admin user to assign yet. Will be set when first admin user is created.")
        
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        db.rollback()
        raise
    finally:
        db.close()

def verify_migration():
    """Verify that the migration was successful"""
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check companies
        companies = db.query(Company).all()
        print(f"\n📊 Migration Verification:")
        print(f"   Companies: {len(companies)}")
        
        # Check data distribution
        for company in companies:
            user_count = db.query(User).filter(User.company_id == company.id).count()
            job_count = db.query(Job).filter(Job.company_id == company.id).count()
            app_count = db.query(Application).filter(Application.company_id == company.id).count()
            
            print(f"   {company.name} (ID: {company.id}):")
            print(f"     Users: {user_count}")
            print(f"     Jobs: {job_count}")
            print(f"     Applications: {app_count}")
            print(f"     Admin: {company.admin_user_id}")
        
        # Check for orphaned records
        orphaned_users = db.query(User).filter(User.company_id.is_(None)).count()
        orphaned_jobs = db.query(Job).filter(Job.company_id.is_(None)).count()
        orphaned_apps = db.query(Application).filter(Application.company_id.is_(None)).count()
        
        if orphaned_users == 0 and orphaned_jobs == 0 and orphaned_apps == 0:
            print("\n✅ Migration successful! No orphaned records found.")
        else:
            print(f"\n⚠️  Found orphaned records:")
            print(f"   Users without company: {orphaned_users}")
            print(f"   Jobs without company: {orphaned_jobs}")
            print(f"   Applications without company: {orphaned_apps}")
        
    finally:
        db.close()

def main():
    """Main migration function"""
    print("🚀 Starting Multi-Company Architecture Migration")
    print("=" * 50)
    
    # Step 1: Backup existing database
    backup_path = backup_database()
    
    # Step 2: Add company_id columns to existing tables
    add_company_columns()
    
    # Step 3: Create companies table and migrate data
    create_default_company_and_migrate_data()
    
    # Step 4: Verify migration
    verify_migration()
    
    print("\n" + "=" * 50)
    print("🎉 Migration completed!")
    if backup_path:
        print(f"💾 Backup saved at: {backup_path}")
    print("🔄 Please restart your application servers.")

if __name__ == "__main__":
    main()