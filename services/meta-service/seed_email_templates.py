#!/usr/bin/env python3
"""
Seed email templates for Meta Portal.
Creates default system email templates in the database.
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from sqlalchemy.orm import Session
from src.config.database import SessionLocal, engine, Base
from src.models.email import EmailTemplate

def create_system_email_templates():
    """Create default system email templates"""
    db = SessionLocal()
    
    try:
        # Create base tables
        Base.metadata.create_all(bind=engine)
        
        templates = [
            {
                "name": "job_application_confirmation",
                "display_name": "Job Application Confirmation",
                "description": "Sent to users when they successfully submit a job application",
                "category": "job",
                "subject_template": "Application Confirmed: {{ job_title }} at {{ company_name }}",
                "text_content": """Dear {{ user_name }},

Thank you for applying to the {{ job_title }} position at {{ company_name }}.

Your application has been successfully received and will be reviewed by our hiring team.

Application Details:
- Position: {{ job_title }}
- Company: {{ company_name }}
- Location: {{ job_location }}
- Application Date: {{ application_date }}
- Application ID: #{{ application_id }}

We will get back to you within {{ review_timeframe or "5-7 business days" }}.

Best regards,
The {{ company_name }} Hiring Team""",
                "html_content": None,  # Will use file template
                "variables": ["user_name", "job_title", "company_name", "job_location", "application_date", "application_id", "review_timeframe", "cover_letter", "dashboard_url"],
                "is_system_template": True,
                "is_active": True
            },
            {
                "name": "application_status_update",
                "display_name": "Application Status Update",
                "description": "Sent when an application status changes",
                "category": "job",
                "subject_template": "Application Update: {{ job_title }} - {{ new_status }}",
                "text_content": """Dear {{ user_name }},

Your application for the {{ job_title }} position at {{ company_name }} has been updated.

New Status: {{ new_status }}
Application ID: #{{ application_id }}
Updated: {{ update_date }}

{% if status_message %}
{{ status_message }}
{% endif %}

{% if next_steps %}
Next Steps:
{% for step in next_steps %}
- {{ step }}
{% endfor %}
{% endif %}

Best regards,
The {{ company_name }} Hiring Team""",
                "html_content": None,
                "variables": ["user_name", "job_title", "company_name", "new_status", "application_id", "update_date", "status_message", "next_steps", "application_url"],
                "is_system_template": True,
                "is_active": True
            },
            {
                "name": "welcome_user",
                "display_name": "Welcome New User",
                "description": "Sent to new users after successful registration",
                "category": "user",
                "subject_template": "Welcome to {{ company_name }}!",
                "text_content": """Dear {{ user_name }},

Welcome to Meta Portal! We're excited to have you join our community.

Your account is now active and you can:
- Complete your profile
- Browse job opportunities
- Apply to positions
- Manage your applications

Account Details:
- Name: {{ user_name }}
- Email: {{ user_email }}
- Registration Date: {{ registration_date }}

Get started: {{ dashboard_url }}

Best regards,
The Meta Portal Team""",
                "html_content": None,
                "variables": ["user_name", "user_email", "registration_date", "dashboard_url", "company_name"],
                "is_system_template": True,
                "is_active": True
            },
            {
                "name": "admin_new_application",
                "display_name": "New Application Alert (Admin)",
                "description": "Sent to admins when a new job application is received",
                "category": "admin",
                "subject_template": "New Application: {{ job_title }}",
                "text_content": """Dear Hiring Manager,

A new application has been received for the {{ job_title }} position.

Application Details:
- Position: {{ job_title }}
- Department: {{ job_department }}
- Location: {{ job_location }}
- Application Date: {{ application_date }}
- Application ID: #{{ application_id }}

Candidate Information:
- Name: {{ candidate_name }}
- Email: {{ candidate_email }}
- Phone: {{ candidate_phone }}
{% if candidate_experience %}
- Experience: {{ candidate_experience }}
{% endif %}

Cover Letter Preview:
{{ cover_letter[:200] }}...

Review the full application: {{ admin_application_url }}

Best regards,
Meta Portal System""",
                "html_content": None,
                "variables": ["job_title", "job_department", "job_location", "application_date", "application_id", "candidate_name", "candidate_email", "candidate_phone", "candidate_experience", "cover_letter", "admin_application_url"],
                "is_system_template": True,
                "is_active": True
            }
        ]
        
        created_count = 0
        for template_data in templates:
            # Check if template already exists
            existing = db.query(EmailTemplate).filter(
                EmailTemplate.name == template_data["name"]
            ).first()
            
            if not existing:
                template = EmailTemplate(**template_data)
                db.add(template)
                created_count += 1
                print(f"✅ Created template: {template_data['name']}")
            else:
                print(f"⚠️  Template already exists: {template_data['name']}")
        
        db.commit()
        
        print(f"\n🎉 Email template seeding completed!")
        print(f"📧 Created {created_count} new templates")
        print(f"📋 Total templates in database: {db.query(EmailTemplate).count()}")
        
    except Exception as e:
        print(f"❌ Error creating email templates: {str(e)}")
        db.rollback()
        raise
    
    finally:
        db.close()

if __name__ == "__main__":
    print("🚀 Seeding email templates...")
    create_system_email_templates()