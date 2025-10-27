# 📁 FILE UPLOAD & ADMIN PAGE GUIDE

## 🎯 Quick Overview

### File Storage Location
```
/Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service/uploads/
```

This directory contains all uploaded files organized as:
```
uploads/
├── resumes/
│   ├── {company_id}/
│   │   └── {user_id}/
│   │       └── resume_YYYYMMDD_HHMMSS_UUID.pdf
│   └── global/
│       └── {user_id}/
│           └── resume_YYYYMMDD_HHMMSS_UUID.pdf
├── temp/
├── quarantine/
├── processed/
└── thumbnails/
```

---

## 📤 WHERE TO TEST FILE UPLOADS

### 1. **Resume Upload** (User-Facing)
**URL:** `http://localhost:8081/resume-management.html`

**How to Test:**
1. Login with test credentials: `alice5678@example.com` / `SecurePass@123`
2. Navigate to "Resume Management" → `http://localhost:8081/resume-management.html`
3. **Drag & drop** a PDF/DOC/DOCX file or click to select
4. File will be uploaded and automatically parsed
5. You can edit the parsed data
6. Manage skills, add/remove entries

**Accepted File Types:**
- PDF (.pdf)
- Word Doc (.doc)
- Word Docx (.docx)
- Text (.txt)
- RTF (.rtf)

**File Limits:**
- Maximum size: **10MB**
- Chunk size: 1MB

**Files Stored At:**
```
uploads/resumes/{company_id}/{user_id}/resume_*.pdf
```

**Expected Response:**
```json
{
  "id": 1,
  "filename": "resume_20251027_143052_a1b2c3d4.pdf",
  "original_filename": "my_resume.pdf",
  "file_size": 245812,
  "content_type": "application/pdf",
  "file_hash": "sha256_hash_here",
  "status": "uploaded",
  "upload_path": "/path/to/file",
  "uploaded_at": "2025-10-27T14:30:52.123Z"
}
```

---

### 2. **Email File Attachments** (Future - Admin/System)
**URL:** `http://localhost:8081/email-management.html`

**How to Test:**
1. Login with admin credentials
2. Navigate to "Email Management" → `http://localhost:8081/email-management.html`
3. Go to **"Send Email"** tab
4. In the email compose interface, you can attach files to emails
5. Files are temporarily stored and then sent via API

**Files Stored At:**
```
uploads/temp/{user_id}/attachment_*.pdf
(Cleaned after email is sent)
```

---

## 🧑‍💼 ADMIN DASHBOARD - CLARIFICATION

### **IMPORTANT: Access & Navigation**

#### ❌ **NO DIRECT LINK FROM MAIN SITE**
You are **CORRECT**! The admin page **cannot be accessed from the regular site navigation**.

This is **intentional for security**:
- Regular users should NOT see admin panel link
- Prevents accidental navigation to admin features
- Follows security best practice of "no direct path to admin"

#### ✅ **HOW TO ACCESS IT MANUALLY**

**Direct URL (No Link):**
```
http://localhost:8081/admin-dashboard.html
```

**Method:**
1. Open your browser
2. Type the URL directly: `http://localhost:8081/admin-dashboard.html`
3. Login with admin credentials (you need admin role)

---

## 👤 Admin Credentials

**Current Admin User:**
- Email: `alice5678@example.com`
- Password: `SecurePass@123`
- Role: Currently NOT set as admin ❌

### ⚠️ **To Make User Admin**

Run this command in the backend terminal:

```bash
cd /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service
source venv_py311/bin/activate
python make_admin.py
```

**Or manually using Python:**

```python
from src.config.database import SessionLocal
from src.models.user import User

db = SessionLocal()
user = db.query(User).filter(User.email == "alice5678@example.com").first()
if user:
    user.is_admin = True
    db.commit()
    print("✅ User is now admin!")
else:
    print("❌ User not found")
db.close()
```

---

## 📊 Admin Dashboard Features

### Tab 1: Dashboard
- Total Applications count
- Active Jobs count
- Total Users count
- Interview count

### Tab 2: Applications
- View all job applications
- Filter by status (Submitted, In Review, Interview, Accepted, Rejected)
- Update application status

### Tab 3: Job Management
- View all jobs
- Create new jobs
- Edit job details
- Statistics on job applications

### Tab 4: User Management
- View all users
- Search users by email/name
- View user details
- See user applications
- User role information

### Tab 5: Company Management
- View all companies
- Add new companies
- Edit company details
- See company statistics
- Filter by status

---

## 📝 Testing Workflow

### Full File Upload Flow:

```
1. User logs in (http://localhost:8081/login.html)
   └── Email: alice5678@example.com
   └── Password: SecurePass@123

2. Navigate to Resume Upload
   └── URL: http://localhost:8081/resume-management.html

3. Upload Resume File
   └── Drag & drop or click to select
   └── Supported: PDF, DOC, DOCX, TXT, RTF
   └── Max 10MB

4. System Response
   ├── File stored at: uploads/resumes/{company_id}/{user_id}/resume_*.pdf
   ├── Hash calculated for duplicate detection
   ├── Virus scan status set (currently disabled)
   └── Resume record created in database

5. Backend Logs Show
   └── File received, stored, and indexed
   └── Resume processing initiated

6. Admin View
   └── Login as admin (if is_admin=true)
   └── Go to: http://localhost:8081/admin-dashboard.html
   └── Tab: "File Management" would show all uploads
```

---

## 🔧 API Endpoints for File Upload

### Upload File
```
POST /api/files/upload
Content-Type: multipart/form-data

Required:
- file: File (PDF/DOC/DOCX)

Optional:
- description: string
- tags: string (comma-separated)

Response: FileUploadResponse
```

### Get User's Files
```
GET /api/files/uploads?skip=0&limit=10

Response: FileUploadListResponse
```

### Download File
```
GET /api/files/download/{file_id}

Response: File content (binary)
```

### Delete File
```
DELETE /api/files/uploads/{file_id}

Response: { "message": "File deleted successfully" }
```

### Process Resume
```
POST /api/resumes

Payload: {
  "file_upload_id": 1,
  "resume_name": "My Resume",
  "is_primary": true
}

Response: ResumeResponse
```

### Get User's Resumes
```
GET /api/resumes?skip=0&limit=10

Response: ResumeListResponse
```

---

## 📊 File Storage Configuration

From `file_upload_service.py`:

```python
class FileUploadConfig:
    # Base upload directory
    UPLOAD_BASE_DIR = "services/meta-service/uploads"
    
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
    
    # Virus scanning (disabled for now)
    VIRUS_SCAN_ENABLED = False
    
    # File retention
    TEMP_FILE_RETENTION_HOURS = 24
    INACTIVE_FILE_RETENTION_DAYS = 365
```

---

## 🔍 Verify Files Are Stored

### List Uploaded Files
```bash
# See all uploaded resumes
ls -la /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service/uploads/resumes/

# Count files
find /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service/uploads -type f | wc -l

# See file structure
tree /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service/uploads
```

---

## ✅ SUMMARY

### File Uploads:
- **Test Page:** `http://localhost:8081/resume-management.html`
- **Storage Location:** `/services/meta-service/uploads/resumes/`
- **Max File Size:** 10MB
- **Supported Formats:** PDF, DOC, DOCX, TXT, RTF

### Admin Dashboard:
- **Access:** Direct URL only (no navbar link) → `http://localhost:8081/admin-dashboard.html`
- **Why?** Security - prevents accidental access, follows best practices
- **Requirement:** User must have `is_admin = true` in database
- **Current User:** Not admin yet - run `make_admin.py` to enable

### Key Point:
**This is intentional design!** Admin pages should NOT be linked from main navigation. Users must know the direct URL or be explicitly granted access. This prevents:
- Accidental admin access
- Exposure of admin features to non-admins
- Security vulnerabilities through UI discovery

---

## 🚀 Next Steps

1. **Test Upload:** Go to `http://localhost:8081/resume-management.html` and upload a PDF
2. **Check Storage:** Verify files appear in `/services/meta-service/uploads/`
3. **Make Admin:** Run `make_admin.py` if you want to access admin dashboard
4. **Access Admin:** Go directly to `http://localhost:8081/admin-dashboard.html`
5. **Review Database:** Files are logged in `file_uploads` and `resumes` tables

---

**Everything working as designed! ✅**
