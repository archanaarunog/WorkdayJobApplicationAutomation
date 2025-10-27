"""
File upload models for Meta Portal.
Handles resume uploads and file management with multi-tenant support.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
import enum

class ResumeStatus(enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing" 
    PROCESSED = "processed"
    FAILED = "failed"
    QUARANTINED = "quarantined"

class UploadStatus(enum.Enum):
    INITIATED = "initiated"
    UPLOADING = "uploading"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class ScanStatus(enum.Enum):
    PENDING = "pending"
    SCANNING = "scanning"
    CLEAN = "clean"
    INFECTED = "infected"
    ERROR = "error"

class StorageBackend(enum.Enum):
    LOCAL = "local"
    S3 = "s3"
    GCS = "gcs"
    AZURE = "azure"

class AccessLevel(enum.Enum):
    PRIVATE = "private"
    COMPANY = "company"
    PUBLIC = "public"

class FileUpload(Base):
    """
    Generic file upload model for all file types
    Base model for managing file uploads with security and tracking
    """
    __tablename__ = "file_uploads"

    id = Column(Integer, primary_key=True, index=True)
    
    # User and Company association
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)
    
    # File Details
    filename = Column(String(500), nullable=False)  # Generated unique filename
    original_name = Column(String(500), nullable=False)  # User's original filename
    file_size = Column(Integer, nullable=False)  # Size in bytes
    mime_type = Column(String(200), nullable=False)
    file_extension = Column(String(10), nullable=False)
    file_hash = Column(String(64), nullable=False, unique=True, index=True)  # SHA256 hash
    
    # Storage Information
    storage_backend = Column(Enum(StorageBackend), default=StorageBackend.LOCAL, nullable=False)
    storage_path = Column(String(1000), nullable=False)  # Full path to file
    storage_bucket = Column(String(200), nullable=True)  # Cloud storage bucket
    storage_key = Column(String(1000), nullable=True)  # Cloud storage key/path
    
    # Upload Process Tracking
    upload_status = Column(Enum(UploadStatus), default=UploadStatus.INITIATED, nullable=False, index=True)
    upload_progress = Column(Integer, default=0, nullable=False)  # Percentage 0-100
    chunk_count = Column(Integer, default=1, nullable=False)  # Total chunks for chunked upload
    chunks_uploaded = Column(Integer, default=0, nullable=False)  # Completed chunks
    
    # Security and Scanning
    virus_scan_status = Column(Enum(ScanStatus), default=ScanStatus.PENDING, nullable=False, index=True)
    virus_scan_result = Column(Text, nullable=True)  # Scan details/errors
    virus_scan_date = Column(DateTime, nullable=True)
    
    # Processing and Metadata
    processing_logs = Column(JSON, nullable=True)  # Processing history and errors
    file_metadata = Column(JSON, nullable=True)  # Additional file metadata
    
    # Access Control and Usage
    access_level = Column(Enum(AccessLevel), default=AccessLevel.PRIVATE, nullable=False)
    download_count = Column(Integer, default=0, nullable=False)
    last_accessed = Column(DateTime, nullable=True)
    
    # Upload Context
    upload_ip = Column(String(45), nullable=True)  # IPv4/IPv6 address
    user_agent = Column(String(500), nullable=True)
    upload_session_id = Column(String(100), nullable=True, index=True)
    
    # File Lifecycle
    expires_at = Column(DateTime, nullable=True)  # Auto-deletion date
    is_temporary = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="uploaded_files")
    company = relationship("Company", back_populates="files")
    resume = relationship("Resume", back_populates="file_upload", uselist=False)

    def __repr__(self):
        return f"<FileUpload(id={self.id}, filename='{self.filename}', status='{self.upload_status.value}', size={self.file_size})>"

class Resume(Base):
    """
    Resume-specific model extending file uploads with resume parsing
    Stores parsed resume data and analysis results
    """
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    
    # File Reference
    file_upload_id = Column(Integer, ForeignKey("file_uploads.id"), nullable=False, unique=True, index=True)
    
    # User and Company association (denormalized for performance)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=True, index=True)
    
    # Processing Status
    status = Column(Enum(ResumeStatus), default=ResumeStatus.UPLOADED, nullable=False, index=True)
    processing_started_at = Column(DateTime, nullable=True)
    processing_completed_at = Column(DateTime, nullable=True)
    processing_duration_ms = Column(Integer, nullable=True)  # Processing time in milliseconds
    
    # Extracted Content
    extracted_text = Column(Text, nullable=True)  # Full text content
    parsed_data = Column(JSON, nullable=True)  # Structured parsed data
    
    # Resume Analysis Results
    skills = Column(JSON, nullable=True)  # Array of identified skills
    experience_years = Column(Integer, nullable=True)  # Calculated years of experience
    education_level = Column(String(100), nullable=True)  # Highest education level
    certifications = Column(JSON, nullable=True)  # Array of certifications
    languages = Column(JSON, nullable=True)  # Array of languages
    
    # Resume Scoring and Matching
    completeness_score = Column(Float, nullable=True)  # 0.0 to 1.0
    quality_score = Column(Float, nullable=True)  # 0.0 to 1.0
    keywords = Column(JSON, nullable=True)  # Extracted keywords for matching
    
    # Personal Information (if extracted)
    candidate_name = Column(String(200), nullable=True)
    candidate_email = Column(String(255), nullable=True)
    candidate_phone = Column(String(50), nullable=True)
    candidate_location = Column(String(200), nullable=True)
    
    # Resume Metadata
    is_primary = Column(Boolean, default=False, nullable=False)  # User's primary resume
    is_active = Column(Boolean, default=True, nullable=False)
    version = Column(Integer, default=1, nullable=False)  # Resume version tracking
    
    # Processing Configuration
    parsing_config = Column(JSON, nullable=True)  # Configuration used for parsing
    ai_analysis_enabled = Column(Boolean, default=True, nullable=False)
    
    # Usage Tracking
    view_count = Column(Integer, default=0, nullable=False)
    download_count = Column(Integer, default=0, nullable=False)
    last_viewed = Column(DateTime, nullable=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    file_upload = relationship("FileUpload", back_populates="resume")
    user = relationship("User", back_populates="resumes")
    company = relationship("Company", back_populates="resumes") 
    application = relationship("Application", back_populates="resume")

    def __repr__(self):
        return f"<Resume(id={self.id}, user_id={self.user_id}, status='{self.status.value}', primary={self.is_primary})>"

class ResumeProcessingLog(Base):
    """
    Detailed logging for resume processing steps
    Tracks processing pipeline for debugging and optimization
    """
    __tablename__ = "resume_processing_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # Resume Reference
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False, index=True)
    
    # Processing Step
    step_name = Column(String(100), nullable=False, index=True)  # text_extraction, skill_parsing, etc.
    step_status = Column(String(50), nullable=False, index=True)  # started, completed, failed
    
    # Timing
    started_at = Column(DateTime, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    duration_ms = Column(Integer, nullable=True)
    
    # Results and Errors
    result_data = Column(JSON, nullable=True)  # Step-specific results
    error_message = Column(Text, nullable=True)
    error_trace = Column(Text, nullable=True)
    
    # Processing Context
    processor_version = Column(String(50), nullable=True)
    processor_config = Column(JSON, nullable=True)
    
    # Audit
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    resume = relationship("Resume", backref="processing_logs")

    def __repr__(self):
        return f"<ResumeProcessingLog(id={self.id}, resume_id={self.resume_id}, step='{self.step_name}', status='{self.step_status}')>"

class FileAccessLog(Base):
    """
    Access logging for file downloads and views
    Security and usage analytics
    """
    __tablename__ = "file_access_logs"

    id = Column(Integer, primary_key=True, index=True)
    
    # File Reference
    file_upload_id = Column(Integer, ForeignKey("file_uploads.id"), nullable=False, index=True)
    
    # Access Details
    access_type = Column(String(50), nullable=False, index=True)  # view, download, preview
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    
    # Request Context
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    referer = Column(String(500), nullable=True)
    
    # Response Details
    response_status = Column(Integer, nullable=False)  # HTTP status code
    bytes_served = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    
    # Audit
    accessed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # Relationships
    file_upload = relationship("FileUpload", backref="access_logs")
    user = relationship("User")

    def __repr__(self):
        return f"<FileAccessLog(id={self.id}, file_id={self.file_upload_id}, type='{self.access_type}', user_id={self.user_id})>"