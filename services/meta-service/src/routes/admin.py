"""
Admin routes for Meta Portal.
Handles admin dashboard, application management, and statistics.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
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
