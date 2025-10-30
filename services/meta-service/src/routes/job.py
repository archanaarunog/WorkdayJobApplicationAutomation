"""
Job routes for Meta Portal API.
Handles job listing endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.config.database import get_db
from src import schemas, models
from src.routes.user import get_current_user, get_user_company_context
from src.utils.multitenant import filter_by_company, auto_set_company_id
from typing import Optional

router = APIRouter(prefix="/api/jobs", tags=["Job"])


@router.get("/", dependencies=[], response_model=list[schemas.JobRead])
def list_jobs(
    db: Session = Depends(get_db),
    company_id: Optional[int] = Query(default=None, description="Optional company filter")
):
    """List active jobs. Public endpoint returns all active jobs; can filter by company_id if provided."""
    query = db.query(models.job.Job).filter(models.job.Job.is_active == True)
    if company_id is not None:
        query = query.filter(models.job.Job.company_id == company_id)
    return query.order_by(models.job.Job.posted_date.desc()).all()

# Create a new job
@router.post("/", response_model=schemas.JobRead)
def create_job(
    job: schemas.JobCreate, 
    db: Session = Depends(get_db),
    current_user: models.user.User = Depends(get_current_user),
    company_context: dict = Depends(get_user_company_context)
):
    """Create a new job posting. User must be admin to create jobs."""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin privileges required to create jobs")
    
    db_job = models.job.Job(**job.dict())
    
    # Set company_id for multi-tenancy
    auto_set_company_id(db, db_job, company_context['company_id'])
    
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job
