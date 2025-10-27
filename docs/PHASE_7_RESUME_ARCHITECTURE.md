# Phase 7 - Resume Upload System Architecture

## Overview
Comprehensive file upload and resume management system for the Meta Job Portal, designed to provide rich testing scenarios for AI automation framework while enhancing user experience.

## File Upload Architecture

### 1. Core Components

#### File Storage Backend
```
uploads/
├── resumes/
│   ├── {company_id}/
│   │   ├── {user_id}/
│   │   │   ├── original/
│   │   │   │   └── {filename}_{timestamp}.{ext}
│   │   │   ├── processed/
│   │   │   │   ├── {file_id}_text.txt
│   │   │   │   ├── {file_id}_metadata.json
│   │   │   │   └── {file_id}_preview.png
│   │   │   └── thumbnails/
│   │   │       └── {file_id}_thumb.jpg
├── temp/
│   └── {session_id}/
└── quarantine/
    └── {suspicious_files}
```

#### File Processing Pipeline
1. **Upload Validation**: File type, size, virus scanning
2. **Metadata Extraction**: File properties, timestamps, hash
3. **Content Processing**: PDF/DOC text extraction, parsing
4. **Resume Analysis**: Skills extraction, experience parsing
5. **Thumbnail Generation**: Preview images for UI
6. **Database Storage**: File metadata and relationships

### 2. Database Models

#### Resume Model
```python
class Resume(Base):
    id: int (Primary Key)
    user_id: int (Foreign Key)
    company_id: int (Foreign Key)
    application_id: int (Foreign Key, Optional)
    
    # File Information
    original_filename: str
    file_size: int
    file_type: str
    file_hash: str (SHA256)
    storage_path: str
    
    # Processing Status
    status: ResumeStatus (UPLOADED, PROCESSING, PROCESSED, FAILED)
    processing_started_at: datetime
    processing_completed_at: datetime
    
    # Extracted Content
    extracted_text: TEXT
    parsed_data: JSON
    skills: JSON
    experience_years: int
    education_level: str
    
    # Metadata
    upload_ip: str
    user_agent: str
    is_primary: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

#### FileUpload Model
```python
class FileUpload(Base):
    id: int (Primary Key)
    user_id: int (Foreign Key)
    company_id: int (Foreign Key)
    
    # File Details
    filename: str
    original_name: str
    file_size: int
    mime_type: str
    file_extension: str
    file_hash: str
    
    # Storage Information
    storage_backend: str (LOCAL, S3, GCS)
    storage_path: str
    storage_bucket: str
    
    # Upload Process
    upload_status: UploadStatus
    upload_progress: int
    chunk_count: int
    chunks_uploaded: int
    
    # Processing
    virus_scan_status: ScanStatus
    virus_scan_result: str
    processing_logs: JSON
    
    # Access Control
    access_level: str (PRIVATE, COMPANY, PUBLIC)
    download_count: int
    last_accessed: datetime
    
    # Audit
    created_at: datetime
    updated_at: datetime
```

### 3. File Upload Service Architecture

#### Upload Strategies
- **Small Files (<10MB)**: Direct upload with progress tracking
- **Large Files (>10MB)**: Chunked upload with resumable capability
- **Batch Upload**: Multiple file handling with queue processing
- **Drag & Drop**: Browser file API integration

#### Security Measures
```python
class FileValidator:
    ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.txt', '.rtf'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    VIRUS_SCAN_ENABLED = True
    
    def validate_file(self, file):
        # File extension validation
        # MIME type verification
        # File size limits
        # Virus scanning
        # Content validation
```

This architecture provides a comprehensive file upload and resume management system that creates rich, realistic testing scenarios for the AI automation framework while delivering valuable functionality to users.

## Overview
Comprehensive file upload system for resumes and documents in Meta Portal, designed to provide rich testing scenarios for AI automation framework.

## Resume Upload Architecture

### 1. Core Components

#### File Storage Layer
- **Local Storage**: Development and testing environment
- **Cloud Storage**: Production (AWS S3, Google Cloud Storage, or Azure Blob)
- **File Organization**: Company-based folder structure with user subfolders
- **Security**: Virus scanning, file validation, access control

#### File Processing Pipeline
```
Upload → Validation → Virus Scan → Storage → Parsing → Metadata Extraction → Database Update
```

#### Document Processing (`services/document_service.py`)
- **Resume Parsing**: Extract text, skills, education, experience
- **File Format Support**: PDF, DOC, DOCX, RTF, TXT
- **Text Extraction**: Using PyPDF2, python-docx, or cloud APIs
- **Metadata Generation**: File size, pages, word count, upload date

### 2. Database Models

#### Resume Model
```python
class Resume(Base):
    id: int (Primary Key)
    user_id: int (Foreign Key)
    application_id: int (Foreign Key, Optional)
    company_id: int (Foreign Key)
    
    # File Information
    original_filename: str
    stored_filename: str
    file_path: str
    file_size_bytes: int
    content_type: str
    file_hash: str  # For duplicate detection
    
    # Document Metadata
    pages: int
    word_count: int
    extracted_text: Text
    
    # Parsing Results
    parsed_skills: JSON
    parsed_experience: JSON
    parsed_education: JSON
    parsed_contact: JSON
    confidence_score: float
    
    # Status and Validation
    status: ResumeStatus (UPLOADING, PROCESSING, ACTIVE, FAILED, DELETED)
    validation_errors: JSON
    virus_scan_result: str
    
    # Usage Tracking
    download_count: int
    last_accessed_at: datetime
    
    # Audit fields
    created_at: datetime
    updated_at: datetime
```

#### FileUpload Model (for tracking all file operations)
```python
class FileUpload(Base):
    id: int (Primary Key)
    user_id: int (Foreign Key)
    company_id: int (Foreign Key)
    
    # Upload Session Information
    upload_session_id: str (UUID)
    chunk_number: int
    total_chunks: int
    chunk_size: int
    
    # File Details
    filename: str
    content_type: str
    file_size: int
    
    # Upload Status
    status: UploadStatus (INITIATED, IN_PROGRESS, COMPLETED, FAILED, CANCELLED)
    progress_percentage: float
    error_message: str
    
    # Processing
    processing_started_at: datetime
    processing_completed_at: datetime
    
    # Audit
    created_at: datetime
    updated_at: datetime
```

### 3. File Upload Strategies

#### Chunked Upload (Large Files)
- **Progressive Upload**: Break large files into smaller chunks
- **Resume Support**: Resume interrupted uploads
- **Real-time Progress**: WebSocket or polling for progress updates
- **Concurrent Processing**: Process chunks as they arrive

#### Direct Upload (Small Files)
- **Single Request**: Files under 10MB
- **Immediate Processing**: Instant validation and storage
- **Quick Feedback**: Immediate success/error response

#### Drag & Drop Interface
- **Multiple File Support**: Batch upload capability
- **Visual Feedback**: Drag zones, progress bars, thumbnails
- **File Validation**: Client-side type/size checking before upload

### 4. File Validation & Security

#### Validation Rules
```python
ALLOWED_EXTENSIONS = {'.pdf', '.doc', '.docx', '.rtf', '.txt'}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB
MIN_FILE_SIZE = 1024  # 1KB
ALLOWED_MIME_TYPES = {
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'text/rtf',
    'text/plain'
}
```

#### Security Measures
- **File Type Validation**: Check both extension and MIME type
- **Virus Scanning**: Integration with ClamAV or cloud security services
- **Content Sanitization**: Remove potentially harmful content
- **Access Control**: User-based and company-based file isolation
- **Rate Limiting**: Prevent abuse with upload frequency limits

### 5. API Endpoints

#### File Upload Endpoints (`/api/files`)
```
POST   /api/files/resume/upload              # Upload resume file
POST   /api/files/resume/upload-chunked      # Chunked upload initiation
PUT    /api/files/resume/upload-chunked/{session_id}/chunk/{chunk}  # Upload chunk
POST   /api/files/resume/upload-chunked/{session_id}/complete       # Complete chunked upload
GET    /api/files/resume/upload-progress/{session_id}               # Get upload progress
DELETE /api/files/resume/upload/{session_id}                       # Cancel upload

GET    /api/files/resume/{resume_id}         # Get resume metadata
GET    /api/files/resume/{resume_id}/download # Download resume file
PUT    /api/files/resume/{resume_id}         # Update resume metadata
DELETE /api/files/resume/{resume_id}        # Delete resume

GET    /api/user/resumes                    # List user's resumes
POST   /api/user/resumes/{resume_id}/set-primary  # Set primary resume
```

#### Admin File Management (`/api/admin/files`)
```
GET    /api/admin/files/resumes             # List all resumes (admin)
GET    /api/admin/files/stats               # File storage statistics
POST   /api/admin/files/cleanup             # Clean up orphaned files
GET    /api/admin/files/uploads             # Monitor active uploads
```

### 6. Frontend Integration

#### Upload Interface Components
- **Drag & Drop Zone**: Visual upload area with file dropping capability
- **File Browser**: Traditional file selection dialog
- **Progress Indicators**: Real-time upload progress with percentage and speed
- **File Preview**: Thumbnail generation for supported formats
- **Upload Queue**: Multiple file upload management

#### Resume Management Interface
- **Resume Library**: Grid/list view of uploaded resumes
- **Quick Actions**: Preview, download, delete, set as primary
- **File Information**: Size, upload date, processing status
- **Integration**: Link resumes to job applications

### 7. AI Testing Framework Benefits

#### Complex File Upload UI Elements
- **Drag & Drop Interactions**: Advanced mouse/touch event handling
- **Progress Bars**: Dynamic content updates and state changes
- **File Type Icons**: Visual element recognition and classification
- **Modal Dialogs**: File preview, confirmation, error handling
- **Form Integration**: Resume selection within job applications

#### Async Processing Scenarios
- **Upload Progress Monitoring**: Real-time status updates
- **Background Processing**: File parsing and validation
- **Error Recovery**: Resume failed uploads, retry mechanisms
- **Multi-step Workflows**: Upload → Process → Parse → Associate

#### Dynamic Element Patterns
- **State-based UI**: Different UI states based on upload/processing status
- **Conditional Rendering**: Show/hide elements based on file type/size
- **Real-time Updates**: WebSocket or polling-based status updates
- **Error Handling**: Various error states and user feedback

### 8. File Processing Pipeline

#### Text Extraction Services
```python
class DocumentProcessor:
    def extract_text(self, file_path: str, file_type: str) -> str
    def parse_resume_sections(self, text: str) -> Dict[str, Any]
    def extract_skills(self, text: str) -> List[str]
    def extract_contact_info(self, text: str) -> Dict[str, str]
    def calculate_confidence_score(self, parsed_data: Dict) -> float
```

#### Integration Options
- **Local Processing**: PyPDF2, python-docx, spaCy for NLP
- **Cloud APIs**: AWS Textract, Google Document AI, Azure Form Recognizer
- **Hybrid Approach**: Local for basic extraction, cloud for advanced parsing

### 9. Storage Configuration

#### Local Development Storage
```python
UPLOAD_DIR = "uploads/"
RESUME_DIR = "uploads/resumes/"
TEMP_DIR = "uploads/temp/"
```

#### Production Cloud Storage
```python
CLOUD_STORAGE = {
    "provider": "aws_s3",  # or "gcs", "azure"
    "bucket_name": "metaportal-files",
    "region": "us-east-1",
    "access_key": "...",
    "secret_key": "..."
}
```

### 10. Performance Considerations

#### Optimization Strategies
- **CDN Integration**: Fast file delivery via CloudFront, CloudFlare
- **Thumbnail Generation**: Quick preview images for documents
- **Lazy Loading**: Load file lists on demand
- **Caching**: Cache processed resume data and extracted text
- **Compression**: Optimize file storage size

#### Scalability Features
- **Background Job Queue**: Celery or Redis for async processing
- **Database Indexing**: Optimize file queries and searches
- **File Deduplication**: Avoid storing identical files multiple times
- **Cleanup Jobs**: Automated removal of temporary and orphaned files

### 11. Monitoring & Analytics

#### File Upload Metrics
- **Upload Success Rate**: Track failed vs successful uploads
- **Processing Performance**: Time to process different file types
- **Storage Usage**: Monitor disk/cloud storage consumption
- **User Behavior**: Most common file types, sizes, usage patterns

#### Error Tracking
- **Upload Failures**: Network issues, file validation errors
- **Processing Errors**: Parsing failures, unsupported formats
- **Security Events**: Virus detection, suspicious file activity
- **Performance Issues**: Slow uploads, processing timeouts

### 12. Testing Scenarios for AI Framework

#### File Upload Testing Patterns
- **Drag and Drop**: Various file types and sizes
- **Batch Upload**: Multiple files simultaneously
- **Progress Monitoring**: Real-time status updates
- **Error Handling**: Network failures, invalid files, size limits
- **Mobile Testing**: Touch-based file selection and upload

#### Resume Management Testing
- **File Association**: Link resumes to job applications
- **File Operations**: Preview, download, delete actions
- **Search and Filter**: Find resumes by name, date, status
- **Responsive Design**: Mobile vs desktop file management

This comprehensive resume upload system provides rich, complex UI interactions and async processing scenarios perfect for training an AI-powered automation framework while serving real business needs for job applications.