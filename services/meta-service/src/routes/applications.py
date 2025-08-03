"""
Application routes for Meta Portal.
Handles job application submission and retrieval for users.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.models.application import Application
from src.models.user import User
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

@router.get("/me", response_model=list[ApplicationRead])
def get_my_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all job applications submitted by the current user.
    """
    return db.query(Application).filter_by(user_id=current_user.id).all()
