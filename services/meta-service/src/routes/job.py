"""
Job routes for Meta Portal API.
Handles job listing endpoints.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.config.database import get_db
from src import schemas, models

router = APIRouter(prefix="/api/jobs", tags=["Job"])


@router.get("/", response_model=list[schemas.JobRead])
def list_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.job.Job).all()
    return jobs

# Create a new job
@router.post("/", response_model=schemas.JobRead)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    db_job = models.job.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job
