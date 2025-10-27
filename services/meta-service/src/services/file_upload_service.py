"""
File Upload Service for Meta Portal.
Handles file uploads, processing, and storage with security and validation.
"""

import os
import hashlib
import mimetypes
import shutil
import uuid
from pathlib import Path
from typing import Optional, Dict, Any, List, BinaryIO
import logging
from datetime import datetime, timedelta

from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session

from ..models.file_upload import (
    FileUpload, Resume, ResumeProcessingLog, FileAccessLog,
    UploadStatus, ScanStatus, ResumeStatus, StorageBackend, AccessLevel
)
from ..models.user import User
from ..config.database import get_db

logger = logging.getLogger(__name__)

class FileUploadConfig:
    """Configuration for file uploads"""
    
    # Base upload directory
    UPLOAD_BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "uploads")
    
    # File size limits (in bytes)
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MAX_CHUNK_SIZE = 1024 * 1024      # 1MB per chunk
    
    # Allowed file types for resumes
    ALLOWED_RESUME_TYPES = {
        'application/pdf': '.pdf',
        'application/msword': '.doc',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document': '.docx',
        'text/plain': '.txt',
        'text/rtf': '.rtf',
        'application/rtf': '.rtf'
    }
    
    # Virus scanning (placeholder for future implementation)
    VIRUS_SCAN_ENABLED = False
    
    # Storage backend
    DEFAULT_STORAGE_BACKEND = StorageBackend.LOCAL
    
    # File retention
    TEMP_FILE_RETENTION_HOURS = 24
    INACTIVE_FILE_RETENTION_DAYS = 365

class FileValidator:
    """File validation utilities"""
    
    @staticmethod
    def validate_file_type(file: UploadFile, allowed_types: Dict[str, str]) -> tuple[bool, str]:
        """Validate file type against allowed types"""
        
        # Check MIME type
        if file.content_type not in allowed_types:
            return False, f"File type '{file.content_type}' not allowed"
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        expected_ext = allowed_types[file.content_type]
        
        if file_ext != expected_ext:
            return False, f"File extension '{file_ext}' doesn't match content type '{file.content_type}'"
        
        return True, "Valid file type"
    
    @staticmethod
    def validate_file_size(file: UploadFile, max_size: int) -> tuple[bool, str]:
        """Validate file size"""
        
        if hasattr(file, 'size') and file.size and file.size > max_size:
            return False, f"File size ({file.size} bytes) exceeds maximum allowed ({max_size} bytes)"
        
        return True, "Valid file size"
    
    @staticmethod
    def calculate_file_hash(file_path: str) -> str:
        """Calculate SHA256 hash of file"""
        hash_sha256 = hashlib.sha256()
        
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            return hash_sha256.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating file hash for {file_path}: {str(e)}")
            return ""

class StorageManager:
    """Manages file storage operations"""
    
    def __init__(self, storage_backend: StorageBackend = StorageBackend.LOCAL):
        self.storage_backend = storage_backend
        self.base_dir = Path(FileUploadConfig.UPLOAD_BASE_DIR)
        
        # Create base directories
        self._create_directories()
    
    def _create_directories(self):
        """Create necessary upload directories"""
        directories = [
            self.base_dir,
            self.base_dir / "resumes",
            self.base_dir / "temp", 
            self.base_dir / "quarantine",
            self.base_dir / "processed",
            self.base_dir / "thumbnails"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def generate_storage_path(
        self, 
        user_id: int, 
        company_id: Optional[int], 
        filename: str, 
        file_type: str = "resumes"
    ) -> Path:
        """Generate organized storage path"""
        
        # Create unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_uuid = str(uuid.uuid4())[:8]
        name, ext = os.path.splitext(filename)
        unique_filename = f"{name}_{timestamp}_{file_uuid}{ext}"
        
        # Organize by company and user
        if company_id:
            path = self.base_dir / file_type / str(company_id) / str(user_id) / unique_filename
        else:
            path = self.base_dir / file_type / "global" / str(user_id) / unique_filename
        
        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        return path
    
    def store_file(self, file: UploadFile, storage_path: Path) -> bool:
        """Store uploaded file to designated path"""
        try:
            with open(storage_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            logger.info(f"File stored successfully at {storage_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error storing file at {storage_path}: {str(e)}")
            return False
    
    def delete_file(self, storage_path: str) -> bool:
        """Delete file from storage"""
        try:
            file_path = Path(storage_path)
            if file_path.exists():
                file_path.unlink()
                logger.info(f"File deleted: {storage_path}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting file {storage_path}: {str(e)}")
            return False
    
    def get_file_info(self, storage_path: str) -> Dict[str, Any]:
        """Get file information from storage"""
        try:
            file_path = Path(storage_path)
            if not file_path.exists():
                return {}
            
            stat = file_path.stat()
            return {
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime),
                "exists": True
            }
        
        except Exception as e:
            logger.error(f"Error getting file info for {storage_path}: {str(e)}")
            return {"exists": False}

class VirusScanner:
    """Virus scanning service (placeholder for future implementation)"""
    
    @staticmethod
    def scan_file(file_path: str) -> tuple[ScanStatus, str]:
        """Scan file for viruses (placeholder implementation)"""
        
        # TODO: Integrate with actual virus scanning service (ClamAV, etc.)
        if FileUploadConfig.VIRUS_SCAN_ENABLED:
            # Simulate virus scanning
            return ScanStatus.CLEAN, "File is clean"
        else:
            return ScanStatus.CLEAN, "Virus scanning disabled"

class FileUploadService:
    """Main file upload service"""
    
    def __init__(self):
        self.storage_manager = StorageManager()
        self.validator = FileValidator()
        self.virus_scanner = VirusScanner()
    
    def upload_resume(
        self,
        db: Session,
        file: UploadFile,
        user: User,
        upload_ip: str = None,
        user_agent: str = None
    ) -> FileUpload:
        """Upload and process resume file"""
        
        try:
            # Validate file type
            is_valid_type, type_message = self.validator.validate_file_type(
                file, FileUploadConfig.ALLOWED_RESUME_TYPES
            )
            if not is_valid_type:
                raise HTTPException(status_code=400, detail=type_message)
            
            # Validate file size
            is_valid_size, size_message = self.validator.validate_file_size(
                file, FileUploadConfig.MAX_FILE_SIZE
            )
            if not is_valid_size:
                raise HTTPException(status_code=400, detail=size_message)
            
            # Generate storage path
            storage_path = self.storage_manager.generate_storage_path(
                user.id, user.company_id, file.filename, "resumes"
            )
            
            # Store file
            if not self.storage_manager.store_file(file, storage_path):
                raise HTTPException(status_code=500, detail="Failed to store file")
            
            # Calculate file hash
            file_hash = self.validator.calculate_file_hash(str(storage_path))
            
            # Check for duplicate files
            existing_file = db.query(FileUpload).filter(
                FileUpload.file_hash == file_hash,
                FileUpload.user_id == user.id
            ).first()
            
            if existing_file:
                # Remove the newly uploaded file and return existing
                self.storage_manager.delete_file(str(storage_path))
                logger.info(f"Duplicate file detected for user {user.id}: {file_hash}")
                return existing_file
            
            # Create file upload record
            file_upload = FileUpload(
                user_id=user.id,
                company_id=user.company_id,
                filename=storage_path.name,
                original_name=file.filename,
                file_size=storage_path.stat().st_size,
                mime_type=file.content_type,
                file_extension=Path(file.filename).suffix.lower(),
                file_hash=file_hash,
                storage_backend=StorageBackend.LOCAL,
                storage_path=str(storage_path),
                upload_status=UploadStatus.COMPLETED,
                upload_progress=100,
                virus_scan_status=ScanStatus.PENDING,
                upload_ip=upload_ip,
                user_agent=user_agent
            )
            
            db.add(file_upload)
            db.commit()
            db.refresh(file_upload)
            
            # Perform virus scan
            scan_status, scan_result = self.virus_scanner.scan_file(str(storage_path))
            file_upload.virus_scan_status = scan_status
            file_upload.virus_scan_result = scan_result
            file_upload.virus_scan_date = datetime.utcnow()
            
            db.commit()
            
            # If file is clean, create resume record and start processing
            if scan_status == ScanStatus.CLEAN:
                resume = self._create_resume_record(db, file_upload)
                # TODO: Start background resume processing
                logger.info(f"Resume uploaded successfully: {resume.id}")
            else:
                logger.warning(f"File failed virus scan: {file_upload.id}")
            
            return file_upload
        
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error uploading resume: {str(e)}")
            db.rollback()
            raise HTTPException(status_code=500, detail="File upload failed")
    
    def _create_resume_record(self, db: Session, file_upload: FileUpload) -> Resume:
        """Create resume record for uploaded file"""
        
        resume = Resume(
            file_upload_id=file_upload.id,
            user_id=file_upload.user_id,
            company_id=file_upload.company_id,
            status=ResumeStatus.UPLOADED
        )
        
        db.add(resume)
        db.commit()
        db.refresh(resume)
        
        return resume
    
    def delete_file(self, db: Session, file_id: int, user: User) -> bool:
        """Delete uploaded file"""
        
        try:
            file_upload = db.query(FileUpload).filter(
                FileUpload.id == file_id,
                FileUpload.user_id == user.id  # Ensure user can only delete their files
            ).first()
            
            if not file_upload:
                raise HTTPException(status_code=404, detail="File not found")
            
            # Delete from storage
            self.storage_manager.delete_file(file_upload.storage_path)
            
            # Delete from database
            db.delete(file_upload)
            db.commit()
            
            logger.info(f"File deleted: {file_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting file {file_id}: {str(e)}")
            db.rollback()
            return False
    
    def get_user_files(
        self,
        db: Session,
        user: User,
        file_type: str = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[FileUpload]:
        """Get user's uploaded files"""
        
        query = db.query(FileUpload).filter(
            FileUpload.user_id == user.id,
            FileUpload.is_active == True
        )
        
        if file_type:
            query = query.filter(FileUpload.mime_type.like(f"{file_type}%"))
        
        return query.order_by(FileUpload.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_file_by_id(self, db: Session, file_id: int, user: User) -> Optional[FileUpload]:
        """Get file by ID with user access check"""
        
        return db.query(FileUpload).filter(
            FileUpload.id == file_id,
            FileUpload.user_id == user.id,
            FileUpload.is_active == True
        ).first()
    
    def log_file_access(
        self,
        db: Session,
        file_upload: FileUpload,
        access_type: str,
        user: Optional[User] = None,
        ip_address: str = None,
        user_agent: str = None,
        response_status: int = 200,
        bytes_served: int = None
    ):
        """Log file access for analytics and security"""
        
        try:
            access_log = FileAccessLog(
                file_upload_id=file_upload.id,
                access_type=access_type,
                user_id=user.id if user else None,
                ip_address=ip_address,
                user_agent=user_agent,
                response_status=response_status,
                bytes_served=bytes_served
            )
            
            db.add(access_log)
            
            # Update file access counters
            if access_type == "download":
                file_upload.download_count += 1
            
            file_upload.last_accessed = datetime.utcnow()
            
            db.commit()
        
        except Exception as e:
            logger.error(f"Error logging file access: {str(e)}")
            db.rollback()

# Global service instance
file_upload_service = FileUploadService()