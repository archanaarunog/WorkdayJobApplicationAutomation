from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status, Response
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import io

from ..config.database import get_db
from ..models.file_upload import FileUpload, Resume, FileAccessLog
from ..models.user import User
from ..services.file_upload_service import FileUploadService
from ..schemas.file_schemas import (
    FileUploadResponse, ResumeResponse, FileUploadListResponse,
    ResumeListResponse, FileUploadStats, ResumeCreate, ResumeUpdate
)
from ..utils.auth import get_current_user, get_current_admin_user

router = APIRouter(prefix="/api/files", tags=["File Upload"])
file_service = FileUploadService()

@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    description: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Upload a file for the current user
    """
    try:
        # Read file content
        file_content = await file.read()
        
        # Process upload through service
        upload_result = await file_service.upload_file(
            file_content=file_content,
            filename=file.filename,
            content_type=file.content_type,
            user_id=current_user.id,
            description=description,
            tags=tags.split(",") if tags else None,
            db=db
        )
        
        return FileUploadResponse(
            id=upload_result.id,
            filename=upload_result.filename,
            original_filename=upload_result.original_filename,
            file_size=upload_result.file_size,
            content_type=upload_result.content_type,
            file_hash=upload_result.file_hash,
            status=upload_result.status,
            upload_path=upload_result.upload_path,
            description=upload_result.description,
            tags=upload_result.tags or [],
            virus_scan_status=upload_result.virus_scan_status,
            virus_scan_result=upload_result.virus_scan_result,
            uploaded_at=upload_result.uploaded_at,
            user_id=upload_result.user_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File upload failed: {str(e)}"
        )

@router.get("/uploads", response_model=FileUploadListResponse)
async def get_user_uploads(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status_filter: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's file uploads with pagination
    """
    query = db.query(FileUpload).filter(FileUpload.user_id == current_user.id)
    
    if status_filter:
        query = query.filter(FileUpload.status == status_filter)
    
    total = query.count()
    uploads = query.offset(skip).limit(limit).all()
    
    return FileUploadListResponse(
        uploads=[
            FileUploadResponse(
                id=upload.id,
                filename=upload.filename,
                original_filename=upload.original_filename,
                file_size=upload.file_size,
                content_type=upload.content_type,
                file_hash=upload.file_hash,
                status=upload.status,
                upload_path=upload.upload_path,
                description=upload.description,
                tags=upload.tags or [],
                virus_scan_status=upload.virus_scan_status,
                virus_scan_result=upload.virus_scan_result,
                uploaded_at=upload.uploaded_at,
                user_id=upload.user_id
            ) for upload in uploads
        ],
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/download/{file_id}")
async def download_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Download a file by ID (user can only download their own files)
    """
    file_upload = db.query(FileUpload).filter(
        FileUpload.id == file_id,
        FileUpload.user_id == current_user.id
    ).first()
    
    if not file_upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    if file_upload.status != "uploaded":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File is not available for download"
        )
    
    # Log file access
    access_log = FileAccessLog(
        file_id=file_id,
        user_id=current_user.id,
        access_type="download",
        ip_address="127.0.0.1"  # In production, get from request
    )
    db.add(access_log)
    db.commit()
    
    file_path = file_upload.upload_path
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found on disk"
        )
    
    return FileResponse(
        path=file_path,
        filename=file_upload.original_filename,
        media_type=file_upload.content_type
    )

@router.delete("/uploads/{file_id}")
async def delete_file(
    file_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a file upload (user can only delete their own files)
    """
    file_upload = db.query(FileUpload).filter(
        FileUpload.id == file_id,
        FileUpload.user_id == current_user.id
    ).first()
    
    if not file_upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    try:
        # Delete file from storage
        await file_service.delete_file(file_upload, db)
        
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file: {str(e)}"
        )

# Resume-specific endpoints
@router.post("/resumes", response_model=ResumeResponse)
async def create_resume_from_upload(
    resume_data: ResumeCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Create a resume record from an uploaded file
    """
    # Verify the file upload belongs to the user
    file_upload = db.query(FileUpload).filter(
        FileUpload.id == resume_data.file_upload_id,
        FileUpload.user_id == current_user.id
    ).first()
    
    if not file_upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File upload not found"
        )
    
    # Check if resume already exists for this file
    existing_resume = db.query(Resume).filter(
        Resume.file_upload_id == resume_data.file_upload_id
    ).first()
    
    if existing_resume:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume already exists for this file"
        )
    
    try:
        # Process resume through service
        resume = await file_service.process_resume(
            file_upload=file_upload,
            resume_name=resume_data.resume_name,
            is_primary=resume_data.is_primary,
            db=db
        )
        
        return ResumeResponse(
            id=resume.id,
            file_upload_id=resume.file_upload_id,
            user_id=resume.user_id,
            resume_name=resume.resume_name,
            is_primary=resume.is_primary,
            parsed_content=resume.parsed_content,
            skills_extracted=resume.skills_extracted or [],
            experience_years=resume.experience_years,
            education_level=resume.education_level,
            processing_status=resume.processing_status,
            processing_error=resume.processing_error,
            created_at=resume.created_at,
            updated_at=resume.updated_at,
            file_upload=FileUploadResponse(
                id=file_upload.id,
                filename=file_upload.filename,
                original_filename=file_upload.original_filename,
                file_size=file_upload.file_size,
                content_type=file_upload.content_type,
                file_hash=file_upload.file_hash,
                status=file_upload.status,
                upload_path=file_upload.upload_path,
                description=file_upload.description,
                tags=file_upload.tags or [],
                virus_scan_status=file_upload.virus_scan_status,
                virus_scan_result=file_upload.virus_scan_result,
                uploaded_at=file_upload.uploaded_at,
                user_id=file_upload.user_id
            )
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Resume processing failed: {str(e)}"
        )

@router.get("/resumes", response_model=ResumeListResponse)
async def get_user_resumes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's resumes with pagination
    """
    query = db.query(Resume).filter(Resume.user_id == current_user.id)
    total = query.count()
    resumes = query.offset(skip).limit(limit).all()
    
    resume_responses = []
    for resume in resumes:
        file_upload = resume.file_upload
        resume_responses.append(
            ResumeResponse(
                id=resume.id,
                file_upload_id=resume.file_upload_id,
                user_id=resume.user_id,
                resume_name=resume.resume_name,
                is_primary=resume.is_primary,
                parsed_content=resume.parsed_content,
                skills_extracted=resume.skills_extracted or [],
                experience_years=resume.experience_years,
                education_level=resume.education_level,
                processing_status=resume.processing_status,
                processing_error=resume.processing_error,
                created_at=resume.created_at,
                updated_at=resume.updated_at,
                file_upload=FileUploadResponse(
                    id=file_upload.id,
                    filename=file_upload.filename,
                    original_filename=file_upload.original_filename,
                    file_size=file_upload.file_size,
                    content_type=file_upload.content_type,
                    file_hash=file_upload.file_hash,
                    status=file_upload.status,
                    upload_path=file_upload.upload_path,
                    description=file_upload.description,
                    tags=file_upload.tags or [],
                    virus_scan_status=file_upload.virus_scan_status,
                    virus_scan_result=file_upload.virus_scan_result,
                    uploaded_at=file_upload.uploaded_at,
                    user_id=file_upload.user_id
                ) if file_upload else None
            )
        )
    
    return ResumeListResponse(
        resumes=resume_responses,
        total=total,
        skip=skip,
        limit=limit
    )

@router.put("/resumes/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: int,
    resume_update: ResumeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update resume information
    """
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    # Update fields
    if resume_update.resume_name is not None:
        resume.resume_name = resume_update.resume_name
    
    if resume_update.is_primary is not None:
        # If setting as primary, unset other primary resumes
        if resume_update.is_primary:
            db.query(Resume).filter(
                Resume.user_id == current_user.id,
                Resume.id != resume_id
            ).update({"is_primary": False})
        resume.is_primary = resume_update.is_primary
    
    db.commit()
    db.refresh(resume)
    
    file_upload = resume.file_upload
    return ResumeResponse(
        id=resume.id,
        file_upload_id=resume.file_upload_id,
        user_id=resume.user_id,
        resume_name=resume.resume_name,
        is_primary=resume.is_primary,
        parsed_content=resume.parsed_content,
        skills_extracted=resume.skills_extracted or [],
        experience_years=resume.experience_years,
        education_level=resume.education_level,
        processing_status=resume.processing_status,
        processing_error=resume.processing_error,
        created_at=resume.created_at,
        updated_at=resume.updated_at,
        file_upload=FileUploadResponse(
            id=file_upload.id,
            filename=file_upload.filename,
            original_filename=file_upload.original_filename,
            file_size=file_upload.file_size,
            content_type=file_upload.content_type,
            file_hash=file_upload.file_hash,
            status=file_upload.status,
            upload_path=file_upload.upload_path,
            description=file_upload.description,
            tags=file_upload.tags or [],
            virus_scan_status=file_upload.virus_scan_status,
            virus_scan_result=file_upload.virus_scan_result,
            uploaded_at=file_upload.uploaded_at,
            user_id=file_upload.user_id
        ) if file_upload else None
    )

@router.delete("/resumes/{resume_id}")
async def delete_resume(
    resume_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete a resume (this will also delete the associated file upload)
    """
    resume = db.query(Resume).filter(
        Resume.id == resume_id,
        Resume.user_id == current_user.id
    ).first()
    
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found"
        )
    
    try:
        # Delete associated file upload
        if resume.file_upload:
            await file_service.delete_file(resume.file_upload, db)
        
        # Delete resume record
        db.delete(resume)
        db.commit()
        
        return {"message": "Resume deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete resume: {str(e)}"
        )

# Admin endpoints
@router.get("/admin/uploads", response_model=FileUploadListResponse)
async def admin_get_all_uploads(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    user_id: Optional[int] = Query(None),
    status_filter: Optional[str] = Query(None),
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Admin endpoint to get all file uploads with filtering
    """
    query = db.query(FileUpload)
    
    if user_id:
        query = query.filter(FileUpload.user_id == user_id)
    
    if status_filter:
        query = query.filter(FileUpload.status == status_filter)
    
    total = query.count()
    uploads = query.offset(skip).limit(limit).all()
    
    return FileUploadListResponse(
        uploads=[
            FileUploadResponse(
                id=upload.id,
                filename=upload.filename,
                original_filename=upload.original_filename,
                file_size=upload.file_size,
                content_type=upload.content_type,
                file_hash=upload.file_hash,
                status=upload.status,
                upload_path=upload.upload_path,
                description=upload.description,
                tags=upload.tags or [],
                virus_scan_status=upload.virus_scan_status,
                virus_scan_result=upload.virus_scan_result,
                uploaded_at=upload.uploaded_at,
                user_id=upload.user_id
            ) for upload in uploads
        ],
        total=total,
        skip=skip,
        limit=limit
    )

@router.get("/admin/stats", response_model=FileUploadStats)
async def admin_get_upload_stats(
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Admin endpoint to get file upload statistics
    """
    total_uploads = db.query(FileUpload).count()
    total_resumes = db.query(Resume).count()
    
    # Status distribution
    pending_uploads = db.query(FileUpload).filter(FileUpload.status == "pending").count()
    uploaded_files = db.query(FileUpload).filter(FileUpload.status == "uploaded").count()
    failed_uploads = db.query(FileUpload).filter(FileUpload.status == "failed").count()
    
    # Virus scan status
    clean_files = db.query(FileUpload).filter(FileUpload.virus_scan_status == "clean").count()
    infected_files = db.query(FileUpload).filter(FileUpload.virus_scan_status == "infected").count()
    pending_scans = db.query(FileUpload).filter(FileUpload.virus_scan_status == "pending").count()
    
    # Total storage used (sum of file sizes)
    total_storage = db.query(FileUpload).with_entities(
        db.func.sum(FileUpload.file_size)
    ).scalar() or 0
    
    return FileUploadStats(
        total_uploads=total_uploads,
        total_resumes=total_resumes,
        pending_uploads=pending_uploads,
        uploaded_files=uploaded_files,
        failed_uploads=failed_uploads,
        clean_files=clean_files,
        infected_files=infected_files,
        pending_scans=pending_scans,
        total_storage_bytes=total_storage
    )

@router.delete("/admin/uploads/{file_id}")
async def admin_delete_file(
    file_id: int,
    current_admin: User = Depends(get_current_admin_user),
    db: Session = Depends(get_db)
):
    """
    Admin endpoint to delete any file upload
    """
    file_upload = db.query(FileUpload).filter(FileUpload.id == file_id).first()
    
    if not file_upload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="File not found"
        )
    
    try:
        # Delete file from storage
        await file_service.delete_file(file_upload, db)
        
        return {"message": "File deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete file: {str(e)}"
        )