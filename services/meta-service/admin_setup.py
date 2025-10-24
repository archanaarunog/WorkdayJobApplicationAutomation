"""
Enhanced Admin Setup Script
Comprehensive tool for setting up admin accounts and test data
"""

import sys
import os
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from src.config.database import engine
from src.models.user import User
from src.models.job import Job
from src.models.application import Application

def show_header():
    """Display script header."""
    print("=" * 60)
    print("🛠️  ADMIN PORTAL SETUP TOOL")
    print("=" * 60)
    print()

def list_all_users(db: Session):
    """List all users in the system."""
    users = db.query(User).all()
    if not users:
        print("❌ No users found in system")
        return []
    
    print(f"\n👥 All Users in System ({len(users)} total):")
    print("-" * 50)
    for i, user in enumerate(users, 1):
        admin_badge = "👑 ADMIN" if user.is_admin else "👤 USER"
        print(f"{i:2d}. {user.email:30s} | {admin_badge}")
        print(f"    Name: {user.first_name} {user.last_name}")
        print()
    
    return users

def make_user_admin(email: str, db: Session):
    """Make a user an admin."""
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
    print(f"   👤 Name: {user.first_name} {user.last_name}")
    return True

def show_system_stats(db: Session):
    """Show current system statistics."""
    users_count = db.query(User).count()
    admin_count = db.query(User).filter(User.is_admin == True).count()
    jobs_count = db.query(Job).count()
    active_jobs = db.query(Job).filter(Job.is_active == True).count()
    applications_count = db.query(Application).count()
    
    print(f"\n📊 System Statistics:")
    print("-" * 30)
    print(f"👥 Total Users:        {users_count}")
    print(f"👑 Admin Users:        {admin_count}")
    print(f"💼 Total Jobs:         {jobs_count}")
    print(f"🟢 Active Jobs:        {active_jobs}")
    print(f"📋 Applications:       {applications_count}")

def show_access_info():
    """Show how to access admin dashboard."""
    print(f"\n🎯 Access Admin Dashboard:")
    print("-" * 30)
    print(f"1. Start servers:")
    print(f"   Backend:  uvicorn src.main:app --reload")
    print(f"   Frontend: python3 -m http.server 8081")
    print(f"")
    print(f"2. Open: http://localhost:8081/admin-dashboard.html")
    print(f"3. Login with your admin account")
    print(f"")
    print(f"📝 Notes:")
    print(f"   • You must logout and login again for admin privileges")
    print(f"   • Admin can see all applications and statistics")
    print(f"   • Admin can update application statuses")

def interactive_mode():
    """Run interactive admin setup."""
    with Session(engine) as db:
        show_header()
        
        while True:
            print("\n🔧 Admin Setup Options:")
            print("1. 👥 List all users")
            print("2. 👑 Make user admin")
            print("3. 📊 Show system stats") 
            print("4. 🎯 Show access info")
            print("5. 🚪 Exit")
            
            choice = input("\nSelect option (1-5): ").strip()
            
            if choice == "1":
                list_all_users(db)
                
            elif choice == "2":
                users = list_all_users(db)
                if users:
                    email = input("\nEnter email to make admin: ").strip()
                    make_user_admin(email, db)
                    
            elif choice == "3":
                show_system_stats(db)
                
            elif choice == "4":
                show_access_info()
                
            elif choice == "5":
                print("\n✅ Setup complete!")
                break
                
            else:
                print("❌ Invalid choice. Please select 1-5.")

def main():
    """Main function."""
    if len(sys.argv) > 1:
        # Command line mode
        email = sys.argv[1]
        with Session(engine) as db:
            show_header()
            make_user_admin(email, db)
            show_access_info()
    else:
        # Interactive mode
        interactive_mode()

if __name__ == "__main__":
    main()