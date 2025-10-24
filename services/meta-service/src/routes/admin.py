"""
Admin routes for Meta Portal.
Handles admin dashboard, application management, and statistics.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional
from src.config.database import get_db
from src.models.user import User
from src.models.application import Application
from src.models.job import Job
from src.routes.user import get_current_user
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


# Get all applications with user and job details
@router.get("/applications")
def get_all_applications(
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Get all applications with user and job information (admin only)."""
    query = db.query(Application).join(User).join(Job)
    
    # Filter by status if provided
    if status and status != "all":
        query = query.filter(Application.status == status)
    
    applications = query.order_by(Application.applied_at.desc()).all()
    
    # Build response with user and job details
    result = []
    for app in applications:
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
                "company": app.job.company,
                "department": app.job.department,
                "location": app.job.location
            }
        })
    
    return result


# Get admin dashboard statistics
@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Get statistics for admin dashboard."""
    total_applications = db.query(Application).count()
    total_jobs = db.query(Job).filter(Job.is_active == True).count()
    total_users = db.query(User).filter(User.is_admin == False).count()
    
    # Count by status
    submitted = db.query(Application).filter(Application.status == "submitted").count()
    in_review = db.query(Application).filter(Application.status == "in_review").count()
    interview = db.query(Application).filter(Application.status == "interview").count()
    accepted = db.query(Application).filter(Application.status == "accepted").count()
    rejected = db.query(Application).filter(Application.status == "rejected").count()
    
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
@router.patch("/applications/{application_id}/status")
def update_application_status(
    application_id: int,
    status_update: ApplicationStatusUpdate,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin)
):
    """Update the status of an application (admin only)."""
    application = db.query(Application).filter(Application.id == application_id).first()
    
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    
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
    admin: User = Depends(get_current_admin)
):
    """Get all jobs with application counts (admin only)."""
    jobs = db.query(Job).order_by(Job.posted_date.desc()).all()
    
    # Add application count for each job
    result = []
    for job in jobs:
        app_count = db.query(Application).filter(Application.job_id == job.id).count()
        result.append({
            "id": job.id,
            "title": job.title,
            "company": job.company,
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
    admin: User = Depends(get_current_admin)
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
    admin: User = Depends(get_current_admin)
):
    """Update a job posting (admin only)."""
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
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
    top_jobs = db.query(Job.id, Job.title, Job.company, 
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
    
    return {
        "top_jobs": [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "application_count": job.app_count
            }
            for job in top_jobs
        ],
        "jobs_without_applications": jobs_no_apps,
        "active_jobs": active_jobs,
        "inactive_jobs": inactive_jobs,
        "total_jobs": active_jobs + inactive_jobs
    }
