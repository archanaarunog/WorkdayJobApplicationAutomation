"""
Application routes for Meta Portal.
Handles job application submission and retrieval for users.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.models.application import Application
from src.models.user import User
from src.models.job import Job
from src.schemas import ApplicationCreate, ApplicationRead
from src.routes.user import get_current_user

router = APIRouter(prefix="/api/applications", tags=["applications"])

@router.post("/", response_model=ApplicationRead)
def apply_to_job(
    application: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit a new job application for the current user.
    Prevents duplicate applications for the same job.
    """
    # Check if already applied
    existing = db.query(Application).filter_by(user_id=current_user.id, job_id=application.job_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already applied to this job")
    app = Application(
        user_id=current_user.id,
        job_id=application.job_id,
        cover_letter=application.cover_letter,
        additional_info=application.additional_info
    )
    db.add(app)
    db.commit()
    db.refresh(app)
    return app

@router.get("/me")
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all job applications submitted by the current user with job details.
    Returns applications with embedded job information for dashboard display.
    """
    applications = db.query(Application).filter_by(user_id=current_user.id).all()
    
    # Enrich applications with job details
    result = []
    for app in applications:
        job = db.query(Job).filter_by(id=app.job_id).first()
        result.append({
            "id": app.id,
            "job_id": app.job_id,
            "cover_letter": app.cover_letter,
            "additional_info": app.additional_info,
            "status": app.status,
            "applied_at": app.applied_at.isoformat(),
            "updated_at": app.updated_at.isoformat() if app.updated_at else None,
            "job": {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "department": job.department,
                "job_type": job.job_type,
                "salary_min": job.salary_min,
                "salary_max": job.salary_max,
                "description": job.description
            } if job else None
        })
    
    return result

@router.patch("/{application_id}/status")
def update_application_status(
    application_id: int,
    status: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update application status (for testing/admin purposes).
    Valid statuses: submitted, in_review, interview, rejected, accepted
    """
    app = db.query(Application).filter_by(id=application_id, user_id=current_user.id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
    
    valid_statuses = ["submitted", "in_review", "interview", "rejected", "accepted"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of: {valid_statuses}")
    
    app.status = status
    db.commit()
    db.refresh(app)
    
    return {"message": "Status updated successfully", "application_id": app.id, "new_status": app.status}
