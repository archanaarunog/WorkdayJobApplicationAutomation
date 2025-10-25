"""
Job routes for Meta Portal API.
Handles job listing endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.config.database import get_db
from src import schemas, models
from src.routes.user import get_current_user, get_user_company_context
from src.utils.multitenant import filter_by_company, auto_set_company_id
from typing import Optional

router = APIRouter(prefix="/api/jobs", tags=["Job"])


@router.get("/", response_model=list[schemas.JobRead])
def list_jobs(
    db: Session = Depends(get_db),
    company_context: Optional[dict] = Depends(get_user_company_context)
):
    """List active jobs. For authenticated users, shows jobs from their company and external jobs if allowed."""
    query = db.query(models.job.Job).filter(models.job.Job.is_active == True)
    
    if company_context and company_context.get('company_id'):
        # For authenticated users, show jobs from their company
        # In future versions, this could be expanded to show external jobs based on company settings
        query = filter_by_company(query, models.job.Job, company_context['company_id'], company_context.get('is_admin', False))
    else:
        # For unauthenticated users, could show public jobs or require authentication
        # For now, require authentication by raising an exception
        raise HTTPException(status_code=401, detail="Authentication required to view jobs")
    
    jobs = query.order_by(models.job.Job.posted_date.desc()).all()
    return jobs

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
