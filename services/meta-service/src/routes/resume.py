"""
Compatibility resume routes to support existing frontend (resume-management.html).
Provides minimal endpoints for fetching a user's resume summary and parsing a resume file.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from src.config.database import get_db
from src.models.file_upload import FileUpload, Resume
from src.models.user import User
from src.routes.user import get_current_user

router = APIRouter(prefix="/api/resumes", tags=["resumes"])


def _resume_to_summary(resume: Resume) -> dict:
    """Convert Resume model to the summary shape expected by the frontend."""
    file_upload: Optional[FileUpload] = resume.file_upload
    # Build a simple parsed summary using available fields; fall back to parsed_data if present
    parsed = resume.parsed_data or {}
    return {
        "file_id": file_upload.id if file_upload else None,
        "name": resume.candidate_name or parsed.get("name"),
        "email": resume.candidate_email or parsed.get("email"),
        "phone": resume.candidate_phone or parsed.get("phone"),
        "skills": resume.skills or parsed.get("skills", []),
        "work_experience": parsed.get("work_experience", []),
        "education": parsed.get("education", []),
        "confidence_score": parsed.get("confidence_score", 0.7),
    }


@router.get("/my-resume")
def get_my_resume(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Return the user's primary or most recent resume in a simplified shape."""
    resume = (
        db.query(Resume)
        .filter(Resume.user_id == current_user.id)
        .order_by(Resume.is_primary.desc(), Resume.updated_at.desc())
        .first()
    )
    if not resume:
        raise HTTPException(status_code=404, detail="No resume found")
    return _resume_to_summary(resume)


@router.post("/parse")
def parse_resume(
    payload: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Minimal parse endpoint: returns stored parsed_data if available.
    Frontend sends { file_id } referencing FileUpload.id.
    """
    file_id = payload.get("file_id")
    if not file_id:
        raise HTTPException(status_code=422, detail="file_id is required")

    file_upload = (
        db.query(FileUpload)
        .filter(FileUpload.id == file_id, FileUpload.user_id == current_user.id)
        .first()
    )
    if not file_upload:
        raise HTTPException(status_code=404, detail="File upload not found")

    resume = db.query(Resume).filter(Resume.file_upload_id == file_upload.id).first()
    if not resume:
        # Create a minimal summary based on file if resume record is missing
        return {
            "file_id": file_upload.id,
            "name": None,
            "email": current_user.email,
            "phone": None,
            "skills": [],
            "work_experience": [],
            "education": [],
            "confidence_score": 0.6,
        }

    return _resume_to_summary(resume)
