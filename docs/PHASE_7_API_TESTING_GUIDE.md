# Phase 7 API Testing Guide - Email & File Upload Systems

## 🚀 Interactive API Testing with Swagger UI

### Prerequisites
- Backend server running on `http://localhost:8000`
- Frontend server running on `http://localhost:8081` (optional)

---

## 1. Access Swagger UI

Open your browser and navigate to: **http://localhost:8000/docs**

You should see the FastAPI interactive documentation with all available endpoints organized by tags:
- **Authentication**
- **Users** 
- **Jobs**
- **Applications**
- **Admin**
- **Email** ✨ (Phase 7)
- **File Upload** ✨ (Phase 7)

---

## 2. Authentication Setup (Required First!)

### Step 1: Register a New User
1. Find `POST /api/users/register` endpoint
2. Click "Try it out"
3. Use this sample data:
```json
{
  "email": "alice5678@example.com",
  "password": "SecurePass@123",
  "first_name": "Aliceia",
  "last_name": "Johnsons",
  "phone": "8056095517"
}
```
4. Click "Execute"
5. Expected response: `201 Created` ✅

### Step 2: Login to Get JWT Token
1. Find `POST /api/users/login` endpoint
2. Click "Try it out"
3. Use this JSON data:
```json
{
  "email": "alice5678@example.com",
  "password": "SecurePass@123"
}
```
4. Click "Execute"
5. **📋 Copy the `access_token` from the response:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhbGljZTU2NzhAZXhhbXBsZS5jb20iLCJjb21wYW55X2lkIjoxLCJ1c2VyX2lkIjo5LCJpc19hZG1pbiI6ZmFsc2UsImV4cCI6MTc2MTU2ODc2N30.PYKfPbMiH4DHn6lnj_PCvjk-EPD-XX-mtibPxx2c7A8
```
- Expected: `200 OK` + access_token

### Step 3: Authorize All Requests
1. **Click the "Authorize" button** at the top of Swagger UI (🔒 icon)
2. In the "HTTPBearer" field, enter: `Bearer YOUR_ACCESS_TOKEN_HERE`
   - Example: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
3. Click "Authorize"
4. Click "Close"

✅ **Now all your API calls will be authenticated!**

---

## 3. Email System Testing

### 3.1 View Email Templates
**Endpoint:** `GET /api/email/templates`
- **Purpose:** See all available email templates
- **Expected:** Should show welcome, job_application, status_update templates

### 3.2 Send Test Email
**Endpoint:** `POST /api/email/send`

**Sample Request:**
```json
{
  "to_email": "recipient@example.com",
  "subject": "Test Email from API",
  "template_name": "welcome",
  "template_data": {
    "user_name": "Test User",
    "company_name": "Meta"
  }
}
```

### 3.3 Check Email Queue
**Endpoints:**
- `GET /api/email/queue` - View pending/sent emails
- `GET /api/email/queue/stats` - Email statistics

### 3.4 Create Custom Template
**Endpoint:** `POST /api/email/templates`

**Sample Request:**
```json
{
  "name": "custom_test",
  "subject": "Custom Test Email - {{user_name}}",
  "html_content": "<h1>Hello {{user_name}}!</h1><p>This is a custom template.</p>",
  "text_content": "Hello {{user_name}}! This is a custom template.",
  "is_active": true
}
```

### 3.5 Email Management (Admin)
**Admin Endpoints:**
- `GET /api/email/admin/statistics` - Email system statistics
- `GET /api/email/admin/queue` - All emails in queue
- `PUT /api/email/admin/templates/{template_id}` - Update templates

---

## 4. File Upload System Testing

### 4.1 Upload a Resume File
**Endpoint:** `POST /api/files/upload`

**Steps:**
1. Find `POST /api/files/upload`
2. Click "Try it out"
3. **Upload a file:**
   - Click "Choose File" and select a PDF or Word document
   - Add description: `"My test resume upload"`
   - Add tags: `"resume,test,pdf"`
4. Click "Execute"
5. **📋 Note the file ID from the response**

**Expected Response:**
```json
{
  "id": 1,
  "filename": "resume_20251027_123456.pdf",
  "original_filename": "my_resume.pdf",
  "file_size": 245760,
  "content_type": "application/pdf",
  "status": "uploaded",
  "virus_scan_status": "clean",
  "uploaded_at": "2025-10-27T12:34:56",
  "user_id": 1
}
```

### 4.2 View Your Uploads
**Endpoint:** `GET /api/files/uploads`
- **Parameters:** `skip=0`, `limit=10` (pagination)
- **Purpose:** See all your uploaded files

### 4.3 Create Resume from Upload
**Endpoint:** `POST /api/files/resumes`

**Sample Request:**
```json
{
  "file_upload_id": 1,
  "resume_name": "My Primary Resume",
  "is_primary": true
}
```

### 4.4 View Your Resumes
**Endpoint:** `GET /api/files/resumes`
- **Purpose:** See all your processed resumes with parsed content

### 4.5 Download File
**Endpoint:** `GET /api/files/download/{file_id}`
- Replace `{file_id}` with actual ID (e.g., `1`)
- **Response:** File download stream

### 4.6 Update Resume
**Endpoint:** `PUT /api/files/resumes/{resume_id}`

**Sample Request:**
```json
{
  "resume_name": "Updated Resume Name",
  "is_primary": false
}
```

### 4.7 Delete Resume/File
**Endpoints:**
- `DELETE /api/files/resumes/{resume_id}` - Delete resume and associated file
- `DELETE /api/files/uploads/{file_id}` - Delete file upload

---

## 5. Admin Features Testing

### 5.1 Create Admin User
First, create an admin user via terminal:
```bash
cd /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service
PYTHONPATH=. ./venv_py311/bin/python make_admin.py
```

### 5.2 Admin File Management
**Endpoints:**
- `GET /api/files/admin/uploads` - View all user uploads
  - **Parameters:** `user_id`, `status_filter`, `skip`, `limit`
- `GET /api/files/admin/stats` - File system statistics
- `DELETE /api/files/admin/uploads/{file_id}` - Delete any file

**Expected Stats Response:**
```json
{
  "total_uploads": 15,
  "total_resumes": 8,
  "pending_uploads": 2,
  "uploaded_files": 13,
  "failed_uploads": 0,
  "clean_files": 15,
  "infected_files": 0,
  "pending_scans": 0,
  "total_storage_bytes": 2457600
}
```

---

## 6. Job Application Workflow Testing

### 6.1 Create a Company (Admin)
**Endpoint:** `POST /api/admin/companies`

**Sample Request:**
```json
{
  "name": "Meta Platforms Inc",
  "description": "Leading social technology company",
  "website": "https://meta.com",
  "industry": "Technology",
  "size": "10000+",
  "location": "Menlo Park, CA"
}
```

### 6.2 Create Job Listings (Admin)
**Endpoint:** `POST /api/admin/jobs`

**Sample Request:**
```json
{
  "title": "Software Engineer",
  "description": "Join our engineering team to build the metaverse...",
  "company_id": 1,
  "department": "Engineering",
  "location": "Remote",
  "employment_type": "Full-time",
  "salary_range": "$120,000 - $180,000",
  "requirements": "Bachelor's degree in CS, 3+ years experience",
  "benefits": "Health insurance, stock options, flexible work"
}
```

### 6.3 Apply to Jobs (User)
**Endpoints:**
- `GET /api/jobs` - View available jobs
- `POST /api/jobs/{job_id}/apply` - Apply to a job with your resume

**Application Request:**
```json
{
  "cover_letter": "I am excited to apply for this position...",
  "resume_id": 1,
  "additional_info": "Available to start immediately"
}
```

---

## 7. Error Testing Scenarios

### 7.1 Authentication Errors
**Test Cases:**
- ❌ Access protected endpoints without token → `401 Unauthorized`
- ❌ Use expired/invalid token → `401 Unauthorized`  
- ❌ Try admin endpoints as regular user → `403 Forbidden`

### 7.2 File Upload Validation
**Test Cases:**
- ❌ Upload oversized file (>10MB) → `400 Bad Request`
- ❌ Upload invalid file type → `400 Bad Request`
- ❌ Try to download someone else's file → `404 Not Found`

### 7.3 Email Validation
**Test Cases:**
- ❌ Send email with invalid email address → `400 Bad Request`
- ❌ Use non-existent template → `404 Not Found`
- ❌ Send without proper authentication → `401 Unauthorized`

---

## 8. Complete Test Flow Example

### 8.1 User Registration & Setup
1. **Register** new user → `POST /api/register`
2. **Login** to get JWT token → `POST /api/login`
3. **Authorize** in Swagger UI → Click 🔒 button

### 8.2 File Upload & Resume Management
1. **Upload resume** → `POST /api/files/upload`
2. **Create resume record** → `POST /api/files/resumes`
3. **View resume list** → `GET /api/files/resumes`
4. **Download file** → `GET /api/files/download/{file_id}`

### 8.3 Email System Testing
1. **View templates** → `GET /api/email/templates`
2. **Send welcome email** → `POST /api/email/send`
3. **Check email queue** → `GET /api/email/queue`
4. **Create custom template** → `POST /api/email/templates`

### 8.4 Job Application Process
1. **View available jobs** → `GET /api/jobs`
2. **Apply to job** → `POST /api/jobs/{job_id}/apply`
3. **Check application status** → `GET /api/applications`

### 8.5 Admin Management
1. **Login as admin** → Use admin credentials
2. **View all uploads** → `GET /api/files/admin/uploads`
3. **Check system stats** → `GET /api/files/admin/stats`
4. **Manage email templates** → Admin email endpoints

---

## 9. Monitoring & Debugging

### 9.1 Server Logs
Monitor the terminal where uvicorn is running for:
- 📋 API requests and responses
- 🗄️ Database queries
- ❌ Error messages
- ⚡ Performance metrics

### 9.2 Database Inspection
```bash
# Check created data
cd /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service
PYTHONPATH=. ./venv_py311/bin/python -c "
from src.config.database import engine
from sqlalchemy import text
with engine.connect() as conn:
    result = conn.execute(text('SELECT name FROM sqlite_master WHERE type=\"table\"'))
    print('📊 Tables:', [row[0] for row in result])
"
```

### 9.3 File System Check
```bash
# Check upload directories
ls -la uploads/
ls -la uploads/resumes/
```

---

## 10. Testing Success Criteria

### ✅ Phase 7 Features Validation

**Email System:**
- [x] Email templates loaded and accessible
- [x] Email sending (queued if no SMTP)
- [x] Template management (admin)
- [x] Email queue monitoring
- [x] Custom template creation

**File Upload System:**
- [x] File upload with validation
- [x] Resume processing and storage
- [x] File download functionality
- [x] Resume management (CRUD)
- [x] Admin file oversight

**Integration:**
- [x] Authentication working across all endpoints
- [x] Proper authorization on protected routes
- [x] Error handling for invalid requests
- [x] Database relationships maintained
- [x] File system operations secure

**Performance:**
- [x] File upload handling large files
- [x] Email queue processing
- [x] Database queries optimized
- [x] API response times acceptable

---

## 11. Next Steps After Testing

### 11.1 Frontend Development
- Build email management UI in admin dashboard
- Create file upload interface with drag & drop
- Integrate email notifications with job workflow

### 11.2 Production Readiness
- Configure SMTP server for email delivery
- Set up cloud file storage (AWS S3, etc.)
- Add comprehensive error logging
- Implement rate limiting and security enhancements

### 11.3 AI Testing Framework Integration
- Use complex file upload flows for AI element testing
- Test email workflows for automated UI validation
- Create test scenarios for AI learning datasets

---

## 📞 Troubleshooting

### Common Issues:
1. **401 Unauthorized:** Check JWT token is properly set in Authorization header
2. **File upload fails:** Verify file size <10MB and supported format
3. **Email not sending:** Check SMTP configuration or expect queued status
4. **Admin endpoints 403:** Ensure user has admin role in database

### Debug Commands:
```bash
# Check server status
curl http://localhost:8000/

# Test authentication endpoint
curl -X POST http://localhost:8000/api/login -F "username=testuser" -F "password=testpass123"

# Check database tables
PYTHONPATH=. ./venv_py311/bin/python -c "from src.config.database import engine; print(engine.table_names())"
```

---

**🎉 Your Phase 7 Email & File Upload System is ready for comprehensive testing!**

**Primary Test URL:** http://localhost:8000/docs