from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime

class FileUploadResponse(BaseModel):
    """Response model for file upload operations"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    filename: str
    original_filename: str
    file_size: int
    content_type: str
    file_hash: str
    status: str
    upload_path: str
    description: Optional[str] = None
    tags: List[str] = []
    virus_scan_status: str
    virus_scan_result: Optional[str] = None
    uploaded_at: datetime
    user_id: int

class FileUploadListResponse(BaseModel):
    """Response model for paginated file upload lists"""
    uploads: List[FileUploadResponse]
    total: int
    skip: int
    limit: int

class ResumeCreate(BaseModel):
    """Request model for creating a resume from uploaded file"""
    file_upload_id: int
    resume_name: str
    is_primary: bool = False

class ResumeUpdate(BaseModel):
    """Request model for updating resume information"""
    resume_name: Optional[str] = None
    is_primary: Optional[bool] = None

class ResumeResponse(BaseModel):
    """Response model for resume operations"""
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    file_upload_id: int
    user_id: int
    resume_name: str
    is_primary: bool
    parsed_content: Optional[str] = None
    skills_extracted: List[str] = []
    experience_years: Optional[int] = None
    education_level: Optional[str] = None
    processing_status: str
    processing_error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    file_upload: Optional[FileUploadResponse] = None

class ResumeListResponse(BaseModel):
    """Response model for paginated resume lists"""
    resumes: List[ResumeResponse]
    total: int
    skip: int
    limit: int

class FileUploadStats(BaseModel):
    """Response model for admin file upload statistics"""
    total_uploads: int
    total_resumes: int
    pending_uploads: int
    uploaded_files: int
    failed_uploads: int
    clean_files: int
    infected_files: int
    pending_scans: int
    total_storage_bytes: int