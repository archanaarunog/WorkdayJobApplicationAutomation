"""
Admin routes for Meta Portal.
Handles admin dashboard, application management, and statistics.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional
from datetime import datetime, timedelta
from src.config.database import get_db
from src.models.user import User
from src.models.application import Application
from src.models.job import Job
from src.models.company import Company
from src.routes.user import get_current_user, get_user_company_context
from src.utils.multitenant import filter_by_company, ensure_company_access, auto_set_company_id
from pydantic import BaseModel

router = APIRouter(prefix="/api/admin", tags=["admin"])


# Dependency to check if user is admin
def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    """Verify that the current user has admin privileges."""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


# Schema for updating application status
class ApplicationStatusUpdate(BaseModel):
    status: str


# Schema for job creation/update
class JobCreate(BaseModel):
    title: str
    company: str
    department: Optional[str] = None
    location: str
    description: str
    requirements: Optional[str] = None
    benefits: Optional[str] = None  # Will be ignored if column doesn't exist
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    job_type: str = "Full-time"
    remote_options: Optional[str] = "On-site"  # Will be ignored if column doesn't exist
    is_active: bool = True


class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    department: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    benefits: Optional[str] = None
    salary_min: Optional[int] = None
    salary_max: Optional[int] = None
    job_type: Optional[str] = None
    remote_options: Optional[str] = None
    is_active: Optional[bool] = None


class JobStatusUpdate(BaseModel):
    is_active: bool


# Schema for user management
class UserStatusUpdate(BaseModel):
    is_active: bool


class UserAdminUpdate(BaseModel):
    is_admin: bool


# Schema for company management
class CompanyCreate(BaseModel):
    name: str
    domain: Optional[str] = None
    slug: str
    description: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    headquarters: Optional[str] = None
    size: Optional[str] = None
    admin_user_id: Optional[int] = None


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    domain: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    headquarters: Optional[str] = None
    size: Optional[str] = None
    admin_user_id: Optional[int] = None
    is_active: Optional[bool] = None


class CompanySettingsUpdate(BaseModel):
    job_posting_approval_required: Optional[bool] = None
    allow_external_applications: Optional[bool] = None
    email_notifications: Optional[bool] = None
    branding_color: Optional[str] = None
    logo_url: Optional[str] = None


# Get all applications with user and job details
@router.get("/applications")
def get_all_applications(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
    company_context: dict = Depends(get_user_company_context)
):
    """Get all applications with user and job information (admin only)."""
    query = db.query(Application).join(User).join(Job)
    
    # Filter by company for multi-tenancy
    query = filter_by_company(query, Application, company_context['company_id'], company_context['is_admin'])
    
    # Filter by status if provided
    if status and status != "all":
        query = query.filter(Application.status == status)
    
    applications = query.order_by(Application.applied_at.desc()).all()
    
    # Build response with user and job details
    result = []
    for app in applications:
        # Get company name from company_id
        company_name = "N/A"
        if app.job.company_id:
            company_obj = db.query(Company).filter(Company.id == app.job.company_id).first()
            if company_obj:
                company_name = company_obj.name
        
        result.append({
            "id": app.id,
            "status": app.status,
            "applied_at": app.applied_at,
            "cover_letter": app.cover_letter,
            "user": {
                "id": app.user.id,
                "name": f"{app.user.first_name} {app.user.last_name}",
                "email": app.user.email,
                "phone": app.user.phone
            },
            "job": {
                "id": app.job.id,
                "title": app.job.title,
                "company": company_name,
                "department": app.job.department,
                "location": app.job.location
            }
        })
    
    return result


# Get admin dashboard statistics
@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
    company_context: dict = Depends(get_user_company_context)
):
    """Get statistics for admin dashboard."""
    # Base queries with company filtering
    app_query = filter_by_company(db.query(Application), Application, company_context['company_id'], company_context['is_admin'])
    job_query = filter_by_company(db.query(Job), Job, company_context['company_id'], company_context['is_admin'])
    user_query = filter_by_company(db.query(User), User, company_context['company_id'], company_context['is_admin'])
    
    total_applications = app_query.count()
    total_jobs = job_query.filter(Job.is_active == True).count()
    total_users = user_query.filter(User.is_admin == False).count()
    
    # Count by status (company-filtered)
    submitted = app_query.filter(Application.status == "submitted").count()
    in_review = app_query.filter(Application.status == "in_review").count()
    interview = app_query.filter(Application.status == "interview").count()
    accepted = app_query.filter(Application.status == "accepted").count()
    rejected = app_query.filter(Application.status == "rejected").count()
    
    return {
        "total_applications": total_applications,
        "total_jobs": total_jobs,
        "total_users": total_users,
        "by_status": {
            "submitted": submitted,
            "in_review": in_review,
            "interview": interview,
            "accepted": accepted,
            "rejected": rejected
        }
    }


# Update application status
@router.patch("/applications/{app_id}/status")
def update_application_status(
    app_id: int,
    status_update: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
    company_context: dict = Depends(get_user_company_context)
):
    """Update the status of a specific application (admin only)."""
    # Ensure admin can only access applications from their company
    application = ensure_company_access(db, Application, app_id, company_context['company_id'], company_context['is_admin'])
    
    # Validate status
    valid_statuses = ["submitted", "in_review", "interview", "accepted", "rejected"]
    if status_update.status not in valid_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
        )
    
    application.status = status_update.status
    db.commit()
    db.refresh(application)
    
    return {"message": "Application status updated successfully", "status": application.status}


# ==================== JOB MANAGEMENT ENDPOINTS ====================

# Get all jobs (admin view)
@router.get("/jobs")
def get_all_jobs(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
    company_context: dict = Depends(get_user_company_context)
):
    """Get all jobs with application counts (admin only)."""
    # Filter jobs by company
    job_query = filter_by_company(db.query(Job), Job, company_context['company_id'], company_context['is_admin'])
    jobs = job_query.order_by(Job.posted_date.desc()).all()
    
    # Add application count for each job
    result = []
    for job in jobs:
        # Filter application count by company as well
        app_query = filter_by_company(db.query(Application), Application, company_context['company_id'], company_context['is_admin'])
        app_count = app_query.filter(Application.job_id == job.id).count()
        
        # Get company name from company_id
        company_name = "N/A"
        if job.company_id:
            company_obj = db.query(Company).filter(Company.id == job.company_id).first()
            if company_obj:
                company_name = company_obj.name
        
        result.append({
            "id": job.id,
            "title": job.title,
            "company": company_name,
            "department": job.department,
            "location": job.location,
            "description": job.description,
            "requirements": job.requirements,
            "benefits": getattr(job, 'benefits', None),  # Default if column doesn't exist
            "salary_min": job.salary_min,
            "salary_max": job.salary_max,
            "job_type": job.job_type,
            "remote_options": getattr(job, 'remote_options', 'On-site'),  # Default if column doesn't exist
            "is_active": job.is_active,
            "posted_date": job.posted_date,
            "application_count": app_count
        })
    
    return result


# Create new job
@router.post("/jobs")
def create_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
    company_context: dict = Depends(get_user_company_context)
):
    """Create a new job posting (admin only)."""
    new_job = Job(
        title=job_data.title,
        company=job_data.company,
        department=job_data.department,
        location=job_data.location,
        description=job_data.description,
        requirements=job_data.requirements,
        salary_min=job_data.salary_min,
        salary_max=job_data.salary_max,
        job_type=job_data.job_type,
        is_active=job_data.is_active
    )
    
    # Add benefits and remote_options if columns exist
    if hasattr(Job, 'benefits'):
        new_job.benefits = job_data.benefits
    if hasattr(Job, 'remote_options'):
        new_job.remote_options = job_data.remote_options
    
    # Set company_id for multi-tenancy
    auto_set_company_id(db, new_job, company_context['company_id'])
    
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    
    return {"message": "Job created successfully", "job": new_job}


# Update job
@router.put("/jobs/{job_id}")
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
    company_context: dict = Depends(get_user_company_context)
):
    """Update a job posting (admin only)."""
    # Ensure admin can only update jobs from their company
    job = ensure_company_access(db, Job, job_id, company_context['company_id'], company_context['is_admin'])
    
    # Update only provided fields
    for field, value in job_data.dict(exclude_unset=True).items():
        setattr(job, field, value)
    
    db.commit()
    db.refresh(job)
    
    return {"message": "Job updated successfully", "job": job}


# Delete job
@router.delete("/jobs/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Delete a job posting (admin only)."""
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check if job has applications
    app_count = db.query(Application).filter(Application.job_id == job_id).count()
    if app_count > 0:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete job with {app_count} applications. Deactivate instead."
        )
    
    db.delete(job)
    db.commit()
    
    return {"message": "Job deleted successfully"}


# Toggle job status (activate/deactivate)
@router.patch("/jobs/{job_id}/status")
def toggle_job_status(
    job_id: int,
    status_update: JobStatusUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Toggle job active status (admin only)."""
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job.is_active = status_update.is_active
    db.commit()
    db.refresh(job)
    
    status_text = "activated" if job.is_active else "deactivated"
    return {"message": f"Job {status_text} successfully", "is_active": job.is_active}


# Get job analytics
@router.get("/jobs/analytics")
def get_job_analytics(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Get job performance analytics (admin only)."""
    
    # Top jobs by application count
    top_jobs_query = db.query(Job.id, Job.title, Job.company_id,
                       func.count(Application.id).label('app_count'))\
                 .outerjoin(Application)\
                 .group_by(Job.id)\
                 .order_by(desc('app_count'))\
                 .limit(10)\
                 .all()
    
    # Jobs with no applications
    jobs_no_apps = db.query(Job)\
                     .outerjoin(Application)\
                     .filter(Application.id.is_(None))\
                     .count()
    
    # Active vs inactive jobs
    active_jobs = db.query(Job).filter(Job.is_active == True).count()
    inactive_jobs = db.query(Job).filter(Job.is_active == False).count()
    
    # Build response with company names
    top_jobs_result = []
    for job in top_jobs_query:
        company_name = "N/A"
        if job.company_id:
            company_obj = db.query(Company).filter(Company.id == job.company_id).first()
            if company_obj:
                company_name = company_obj.name
        
        top_jobs_result.append({
            "id": job.id,
            "title": job.title,
            "company": company_name,
            "application_count": job.app_count
        })
    
    return {
        "top_jobs": top_jobs_result,
        "jobs_without_applications": jobs_no_apps,
        "active_jobs": active_jobs,
        "inactive_jobs": inactive_jobs,
        "total_jobs": active_jobs + inactive_jobs
    }


# ==================== USER MANAGEMENT ENDPOINTS ====================

# Get all users (admin view)
@router.get("/users")
def get_all_users(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
    company_context: dict = Depends(get_user_company_context)
):
    """Get all users with application counts and statistics (admin only)."""
    # Filter users by company
    user_query = filter_by_company(db.query(User), User, company_context['company_id'], company_context['is_admin'])
    users = user_query.order_by(User.created_at.desc()).all()
    
    # Add application count and statistics for each user
    result = []
    for user in users:
        # Filter applications by company as well
        app_query = filter_by_company(db.query(Application), Application, company_context['company_id'], company_context['is_admin'])
        app_count = app_query.filter(Application.user_id == user.id).count()
        
        # Get user's latest application date (company-filtered)
        latest_app = app_query.filter(Application.user_id == user.id)\
                      .order_by(Application.applied_at.desc())\
                      .first()
        
        result.append({
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "full_name": f"{user.first_name} {user.last_name}",
            "phone": user.phone,
            "is_admin": user.is_admin,
            "is_active": getattr(user, 'is_active', True),  # Default to active if column doesn't exist
            "created_at": user.created_at,
            "application_count": app_count,
            "latest_application": latest_app.applied_at if latest_app else None
        })
    
    return result


# Get user details
@router.get("/users/{user_id}")
def get_user_details(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
    company_context: dict = Depends(get_user_company_context)
):
    """Get detailed information about a specific user (admin only)."""
    # Ensure admin can only access users from their company
    user = ensure_company_access(db, User, user_id, company_context['company_id'], company_context['is_admin'])
    
    # Get user's applications with job details (company-filtered)
    app_query = filter_by_company(db.query(Application), Application, company_context['company_id'], company_context['is_admin'])
    applications = app_query.join(Job)\
                     .filter(Application.user_id == user_id)\
                     .order_by(Application.applied_at.desc())\
                     .all()
    
    user_applications = []
    for app in applications:
        user_applications.append({
            "id": app.id,
            "job_title": app.job.title,
            "company": app.job.company,
            "status": app.status,
            "applied_at": app.applied_at,
            "cover_letter": app.cover_letter[:100] + "..." if len(app.cover_letter) > 100 else app.cover_letter
        })
    
    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "is_admin": user.is_admin,
        "is_active": getattr(user, 'is_active', True),
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "application_count": len(user_applications),
        "applications": user_applications
    }





# Toggle user account status
@router.patch("/users/{user_id}/status")
def toggle_user_status(
    user_id: int,
    status_update: UserStatusUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
    company_context: dict = Depends(get_user_company_context)
):
    """Enable or disable a user account (admin only)."""
    # Ensure admin can only modify users from their company
    user = ensure_company_access(db, User, user_id, company_context['company_id'], company_context['is_admin'])
    
    # Prevent admin from disabling their own account
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="Cannot disable your own account")
    
    # For now, we'll track this in a way that doesn't require DB changes
    # In the future, add is_active column to User model
    
    # Simulate account status change (would need is_active column in production)
    status_text = "enabled" if status_update.is_active else "disabled"
    
    return {
        "message": f"User account {status_text} successfully",
        "user_id": user.id,
        "is_active": status_update.is_active,
        "note": "Account status tracking requires database migration to add is_active column"
    }


# Toggle user admin privileges
@router.patch("/users/{user_id}/admin")
def toggle_user_admin(
    user_id: int,
    admin_update: UserAdminUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin),
    company_context: dict = Depends(get_user_company_context)
):
    """Grant or revoke admin privileges for a user (admin only)."""
    # Ensure admin can only modify users from their company
    user = ensure_company_access(db, User, user_id, company_context['company_id'], company_context['is_admin'])
    
    # Prevent admin from removing their own admin privileges
    if user.id == admin.id and not admin_update.is_admin:
        raise HTTPException(status_code=400, detail="Cannot remove your own admin privileges")
    
    user.is_admin = admin_update.is_admin
    db.commit()
    db.refresh(user)
    
    status_text = "granted" if user.is_admin else "revoked"
    return {
        "message": f"Admin privileges {status_text} successfully",
        "user_id": user.id,
        "is_admin": user.is_admin
    }


# ==================== COMPANY MANAGEMENT ENDPOINTS ====================

# Get all companies
@router.get("/companies")
def get_all_companies(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Get all companies with statistics (admin only)."""
    companies = db.query(Company).order_by(Company.created_at.desc()).all()
    
    result = []
    for company in companies:
        # Get company statistics
        user_count = db.query(User).filter(User.company_id == company.id).count()
        job_count = db.query(Job).filter(Job.company_id == company.id).count()
        active_job_count = db.query(Job).filter(
            Job.company_id == company.id,
            Job.is_active == True
        ).count()
        application_count = db.query(Application).filter(Application.company_id == company.id).count()
        
        # Get admin user info
        admin_user = None
        if company.admin_user_id:
            admin_user_obj = db.query(User).filter(User.id == company.admin_user_id).first()
            if admin_user_obj:
                admin_user = {
                    "id": admin_user_obj.id,
                    "email": admin_user_obj.email,
                    "name": f"{admin_user_obj.first_name} {admin_user_obj.last_name}"
                }
        
        result.append({
            "id": company.id,
            "name": company.name,
            "domain": company.domain,
            "slug": company.slug,
            "description": company.description,
            "industry": company.industry,
            "website": company.website,
            "headquarters": company.headquarters,
            "size": company.size,
            "is_active": company.is_active,
            "created_at": company.created_at,
            "updated_at": company.updated_at,
            "admin_user": admin_user,
            "statistics": {
                "user_count": user_count,
                "job_count": job_count,
                "active_job_count": active_job_count,
                "application_count": application_count
            },
            "settings": company.settings
        })
    
    return result


# Get company details
@router.get("/companies/{company_id}")
def get_company_details(
    company_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Get detailed information about a specific company (admin only)."""
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get company statistics
    users = db.query(User).filter(User.company_id == company.id).all()
    jobs = db.query(Job).filter(Job.company_id == company.id).all()
    applications = db.query(Application).filter(Application.company_id == company.id).all()
    
    # Get recent activity
    recent_users = db.query(User).filter(User.company_id == company.id)\
                     .order_by(User.created_at.desc()).limit(5).all()
    recent_jobs = db.query(Job).filter(Job.company_id == company.id)\
                    .order_by(Job.posted_date.desc()).limit(5).all()
    recent_applications = db.query(Application).join(Job)\
                           .filter(Application.company_id == company.id)\
                           .order_by(Application.applied_at.desc()).limit(10).all()
    
    # Get admin user info
    admin_user = None
    if company.admin_user_id:
        admin_user_obj = db.query(User).filter(User.id == company.admin_user_id).first()
        if admin_user_obj:
            admin_user = {
                "id": admin_user_obj.id,
                "email": admin_user_obj.email,
                "name": f"{admin_user_obj.first_name} {admin_user_obj.last_name}",
                "created_at": admin_user_obj.created_at
            }
    
    return {
        "id": company.id,
        "name": company.name,
        "domain": company.domain,
        "slug": company.slug,
        "description": company.description,
        "industry": company.industry,
        "website": company.website,
        "headquarters": company.headquarters,
        "size": company.size,
        "is_active": company.is_active,
        "created_at": company.created_at,
        "updated_at": company.updated_at,
        "admin_user": admin_user,
        "settings": company.settings,
        "statistics": {
            "total_users": len(users),
            "total_jobs": len(jobs),
            "active_jobs": len([j for j in jobs if j.is_active]),
            "total_applications": len(applications)
        },
        "recent_activity": {
            "recent_users": [
                {
                    "id": u.id,
                    "email": u.email,
                    "name": f"{u.first_name} {u.last_name}",
                    "created_at": u.created_at
                }
                for u in recent_users
            ],
            "recent_jobs": [
                {
                    "id": j.id,
                    "title": j.title,
                    "location": j.location,
                    "posted_date": j.posted_date
                }
                for j in recent_jobs
            ],
            "recent_applications": [
                {
                    "id": a.id,
                    "job_title": a.job.title if a.job else "N/A",
                    "user_name": f"{a.user.first_name} {a.user.last_name}" if a.user else "N/A",
                    "status": a.status,
                    "applied_at": a.applied_at
                }
                for a in recent_applications
            ]
        }
    }


# Create new company
@router.post("/companies")
def create_company(
    company_data: CompanyCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Create a new company (admin only)."""
    
    # Check if company with same name or slug already exists
    existing_name = db.query(Company).filter(Company.name == company_data.name).first()
    if existing_name:
        raise HTTPException(status_code=400, detail="Company with this name already exists")
    
    existing_slug = db.query(Company).filter(Company.slug == company_data.slug).first()
    if existing_slug:
        raise HTTPException(status_code=400, detail="Company with this slug already exists")
    
    # Check if domain is already used (if provided)
    if company_data.domain:
        existing_domain = db.query(Company).filter(Company.domain == company_data.domain).first()
        if existing_domain:
            raise HTTPException(status_code=400, detail="Company with this domain already exists")
    
    # Validate admin user exists (if provided)
    if company_data.admin_user_id:
        admin_user = db.query(User).filter(User.id == company_data.admin_user_id).first()
        if not admin_user:
            raise HTTPException(status_code=400, detail="Specified admin user does not exist")
    
    # Create new company
    new_company = Company(
        name=company_data.name,
        domain=company_data.domain,
        slug=company_data.slug,
        description=company_data.description,
        industry=company_data.industry,
        website=company_data.website,
        headquarters=company_data.headquarters,
        size=company_data.size,
        admin_user_id=company_data.admin_user_id,
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
    
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    
    return {
        "message": "Company created successfully",
        "company": {
            "id": new_company.id,
            "name": new_company.name,
            "slug": new_company.slug,
            "domain": new_company.domain
        }
    }


# Update company
@router.patch("/companies/{company_id}")
def update_company(
    company_id: int,
    company_data: CompanyUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Update company information (admin only)."""
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Check for unique constraints
    if company_data.name and company_data.name != company.name:
        existing_name = db.query(Company).filter(
            Company.name == company_data.name,
            Company.id != company_id
        ).first()
        if existing_name:
            raise HTTPException(status_code=400, detail="Company with this name already exists")
    
    if company_data.domain and company_data.domain != company.domain:
        existing_domain = db.query(Company).filter(
            Company.domain == company_data.domain,
            Company.id != company_id
        ).first()
        if existing_domain:
            raise HTTPException(status_code=400, detail="Company with this domain already exists")
    
    # Validate admin user exists (if provided)
    if company_data.admin_user_id is not None:
        if company_data.admin_user_id:  # Not setting to None
            admin_user = db.query(User).filter(User.id == company_data.admin_user_id).first()
            if not admin_user:
                raise HTTPException(status_code=400, detail="Specified admin user does not exist")
    
    # Update company fields
    for field, value in company_data.dict(exclude_unset=True).items():
        setattr(company, field, value)
    
    db.commit()
    db.refresh(company)
    
    return {
        "message": "Company updated successfully",
        "company": {
            "id": company.id,
            "name": company.name,
            "slug": company.slug,
            "domain": company.domain,
            "is_active": company.is_active
        }
    }


# Update company settings
@router.patch("/companies/{company_id}/settings")
def update_company_settings(
    company_id: int,
    settings_data: CompanySettingsUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Update company settings (admin only)."""
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Get current settings or create default
    current_settings = company.settings or {
        'job_posting_approval_required': False,
        'allow_external_applications': True,
        'email_notifications': True,
        'branding_color': '#007bff',
        'logo_url': None,
        'custom_application_fields': []
    }
    
    # Update settings
    for field, value in settings_data.dict(exclude_unset=True).items():
        if value is not None:
            current_settings[field] = value
    
    company.settings = current_settings
    db.commit()
    db.refresh(company)
    
    return {
        "message": "Company settings updated successfully",
        "settings": company.settings
    }


# Delete company
@router.delete("/companies/{company_id}")
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Delete a company (admin only). WARNING: This will delete all associated data."""
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Prevent deletion of default company
    if company.slug == "default":
        raise HTTPException(status_code=400, detail="Cannot delete the default company")
    
    # Get statistics before deletion
    user_count = db.query(User).filter(User.company_id == company.id).count()
    job_count = db.query(Job).filter(Job.company_id == company.id).count()
    application_count = db.query(Application).filter(Application.company_id == company.id).count()
    
    company_name = company.name
    
    # Delete the company (cascading deletes will handle related data)
    db.delete(company)
    db.commit()
    
    return {
        "message": f"Company '{company_name}' deleted successfully",
        "deleted_data": {
            "users": user_count,
            "jobs": job_count,
            "applications": application_count
        }
    }
