# Phase 7 Frontend UI Implementation Plan

**Status:** IN PROGRESS  
**Last Updated:** October 27, 2025  
**Target Completion:** Complete

---

## 📋 Overview

Phase 7 backend is **100% complete** with working email and file upload APIs. This document outlines the remaining frontend UI work needed to fully implement Phase 7 features for end-users.

---

## 🎯 What's Already Done (Backend)

### ✅ Email System (Backend Complete)
- Email templates (welcome, job confirmation, status updates, etc.)
- Email sending with SMTP integration
- Email queue management
- Email history tracking
- Admin statistics dashboard (API available)

**Available APIs:**
- `GET /api/email/templates` - List all email templates
- `POST /api/email/send` - Send email notification
- `GET /api/email/queue` - Check pending emails
- `GET /api/admin/email/statistics` - Email metrics

### ✅ File Upload System (Backend Complete)
- File upload validation (type, size, virus scan framework)
- Resume parsing and storage
- File download/retrieval
- Admin file management
- File access logging

**Available APIs:**
- `POST /api/files/upload` - Upload file/resume
- `GET /api/files/{file_id}` - Retrieve file metadata
- `GET /api/files/download/{file_id}` - Download file
- `DELETE /api/files/{file_id}` - Delete file
- `POST /api/resumes/parse` - Parse resume

---

## 🏗️ Frontend UI Work Remaining

### **PHASE 7A: Email Management Frontend** (Priority: HIGH)

#### Feature 1: Email Templates Manager (Admin Only)
**Location:** `admin-dashboard.html` → New "Email Templates" tab  
**Components:**
1. **Template List Section**
   - Display all email templates in a table
   - Columns: Template Name, Subject, Last Modified, Actions
   - Search/filter templates
   - Create new template button

2. **Template Editor Modal**
   - Template name (read-only)
   - Subject line (editable)
   - Email body (rich text editor or textarea)
   - Preview button (shows how email looks)
   - Save & Cancel buttons

3. **Design Elements**
   - Clean form layout
   - Syntax highlighting for template variables
   - Sample variables reference (e.g., {user_name}, {job_title})
   - Success/error notifications

**Technical Details:**
- Call `GET /api/email/templates` on page load
- Store templates in JavaScript
- On edit, POST to backend to update
- Show loading spinner during save

---

#### Feature 2: Email Sending Interface (Admin Only)
**Location:** `admin-dashboard.html` → New "Send Email" tab  
**Components:**
1. **Email Composer**
   - Recipient selection (all users, specific user, or manual entry)
   - Template selector dropdown
   - Subject field (pre-filled from template)
   - Email body (pre-filled from template, editable)
   - Preview button

2. **Send Controls**
   - Send Now button
   - Schedule for Later (optional)
   - Add attachments (optional)
   - Success confirmation message

3. **Queue Display**
   - Show pending emails in a small card
   - Live count update
   - Link to "Email Queue" section

**Technical Details:**
- Call `GET /api/email/templates` to populate dropdown
- On send, POST to `/api/email/send`
- Poll `/api/email/queue` to show pending count
- Display success/error toast messages

---

#### Feature 3: Email Queue Monitor (Admin Only)
**Location:** `admin-dashboard.html` → New "Email Queue" tab  
**Components:**
1. **Queue Table**
   - Display all pending emails
   - Columns: Recipient, Subject, Status, Scheduled Time, Actions
   - Retry failed button
   - Cancel pending button
   - Auto-refresh every 5 seconds

2. **Queue Statistics**
   - Total pending
   - Total failed
   - Total sent today
   - Success rate percentage

3. **Filters**
   - Filter by status (pending, sent, failed)
   - Date range filter
   - Recipient search

**Technical Details:**
- Call `GET /api/email/queue` on load and every 5 seconds
- Call `GET /api/admin/email/statistics` for metrics
- Implement auto-refresh with loading indicator
- Use color-coded status badges

---

#### Feature 4: Email History (Admin Only)
**Location:** `admin-dashboard.html` → New "Email History" tab  
**Components:**
1. **Email Log Table**
   - All sent emails with details
   - Columns: Recipient, Subject, Sent Date/Time, Status, Template Used
   - Search by recipient
   - Filter by date range
   - Filter by template

2. **Email Detail View**
   - Click row to see full email content
   - Show delivery status
   - Show any error messages
   - Resend option

3. **Export Feature**
   - Export to CSV button
   - Export date range selection

**Technical Details:**
- Store email history in state/backend query
- Implement pagination if list is large
- Use Bootstrap table styling
- Add modal for detail view

---

### **PHASE 7B: Resume Upload Frontend** (Priority: HIGH)

#### Feature 1: Resume Upload Component (User Dashboard)
**Location:** `dashboard.html` → New "My Resume" section  
**Components:**
1. **Drag-and-Drop Area**
   - Large drop zone with dashed border
   - "Drag resume here or click to browse" text
   - Accept file types: .pdf, .doc, .docx
   - Max file size display (e.g., "Max 5MB")

2. **File Input**
   - Hidden file input for click-to-browse
   - File validation on client-side
     - Check file type
     - Check file size
     - Show clear error messages

3. **Upload Progress**
   - Progress bar showing upload percentage
   - File size display
   - Estimated time remaining (optional)
   - Cancel upload button during progress

4. **Upload Result**
   - Success message with checkmark
   - File details display (name, size, upload date)
   - Preview button (if supported)
   - Delete button
   - Replace/Upload New button

**Technical Details:**
- Use FormData API for multipart file upload
- Implement drag-and-drop with `ondrop` and `ondragover`
- Client-side validation before sending
- POST to `/api/files/upload`
- Show success toast message
- Store file_id in state for future use

**Validation Rules:**
```
- Accepted formats: .pdf, .doc, .docx
- Max file size: 5MB
- No virus/malware (backend handles)
```

---

#### Feature 2: Resume Parser Display (User Dashboard)
**Location:** `dashboard.html` → Resume section (after upload)  
**Components:**
1. **Parsed Resume Data Display**
   - Extracted information from resume:
     - Name
     - Email
     - Phone
     - Skills (extracted list)
     - Work experience summary
     - Education summary
   - Edit extracted data option

2. **Skills Management**
   - Display extracted skills as tags
   - Add/remove skills manually
   - Save skills to profile

3. **Resume Preview**
   - View uploaded file
   - Download original file
   - View parsing confidence (optional)

**Technical Details:**
- After upload success, call `/api/resumes/parse`
- Display parsed JSON data in formatted sections
- Allow editing extracted data
- Save changes back to backend

---

#### Feature 3: Resume Status in Job Application (User Dashboard)
**Location:** Job application modal  
**Components:**
1. **Resume Selection During Application**
   - When applying for a job, show:
     - "Use saved resume" checkbox (if resume exists)
     - Or "Upload new resume" option
   - If saved resume exists, auto-select it
   - Show resume name and upload date

2. **Resume Management Link**
   - Link to "Manage Resume" section
   - Quick upload option right in modal

**Technical Details:**
- On application modal open, check if user has resume
- If yes, pre-populate selection
- Allow override with new upload
- Send file_id with application submission

---

#### Feature 4: Admin Resume Management (Admin Dashboard)
**Location:** `admin-dashboard.html` → New "Resumes" tab  
**Components:**
1. **Resume List (All Users)**
   - Table with columns: User, File Name, Upload Date, Status, Actions
   - View button (see parsed data)
   - Download button
   - Delete button (admin only)

2. **Resume Statistics**
   - Total resumes uploaded
   - Resumes by format (.pdf, .doc, .docx)
   - Parse success rate
   - Recent uploads

3. **Bulk Actions** (Optional)
   - Download multiple resumes as zip
   - Delete multiple resumes

**Technical Details:**
- Query backend for all resumes
- Display in paginated table
- Implement view modal for parsed data
- Use Bootstrap icons for actions

---

## 📋 Implementation Checklist

### **Phase 7A: Email UI**
- [ ] Create Email Templates Manager tab
  - [ ] Display template list
  - [ ] Create template editor modal
  - [ ] Implement template save functionality
  
- [ ] Create Email Sending Interface
  - [ ] Build email composer form
  - [ ] Implement template selection
  - [ ] Add send functionality
  
- [ ] Create Email Queue Monitor
  - [ ] Build queue table
  - [ ] Implement auto-refresh
  - [ ] Add statistics cards
  
- [ ] Create Email History View
  - [ ] Build email log table
  - [ ] Add search/filter
  - [ ] Create detail modal

### **Phase 7B: Resume Upload UI**
- [ ] Create Drag-and-Drop Upload Component
  - [ ] Build drop zone UI
  - [ ] Implement drag-and-drop handlers
  - [ ] Add file validation
  - [ ] Show progress bar
  
- [ ] Create Resume Parser Display
  - [ ] Display parsed data sections
  - [ ] Implement skills management
  - [ ] Add preview functionality
  
- [ ] Integrate Resume in Job Application
  - [ ] Add resume selection to modal
  - [ ] Show resume status
  - [ ] Handle resume in application submit
  
- [ ] Create Admin Resume Management
  - [ ] Build resume list table
  - [ ] Add statistics display
  - [ ] Implement bulk actions

---

## 🎨 Design System Standards

All new UI components should follow:

**Color Scheme:**
- Primary: Pastel purple (#7C5BA6, #8B6BA8)
- Secondary: Light lavender (#E8DFF5, #F0E8F8)
- Success: Green (#5BA85C)
- Error: Red (#D9534F)
- Text: Dark gray (#333333)

**Components:**
- Use Bootstrap 5 framework
- Purple buttons for actions
- Consistent card styling with shadow
- Hover effects on interactive elements
- Smooth transitions (0.3s)

**Layout:**
- 12-column grid layout
- Consistent padding: 20px
- Max content width: 1200px
- Responsive on mobile (stack vertically)

**Icons:**
- Use Bootstrap Icons (bi class)
- Consistent icon sizing
- Color icons to match status/context

---

## 🔗 API Integration Points

### Email APIs
```javascript
// Get templates
GET /api/email/templates

// Send email
POST /api/email/send
Body: {
  recipient: "user@example.com",
  template_id: 1,
  subject: "Custom Subject",
  body: "Email content"
}

// Get queue
GET /api/email/queue

// Get statistics
GET /api/admin/email/statistics
```

### File Upload APIs
```javascript
// Upload file
POST /api/files/upload
Body: FormData (multipart/form-data)

// Get file
GET /api/files/{file_id}

// Download file
GET /api/files/download/{file_id}

// Delete file
DELETE /api/files/{file_id}

// Parse resume
POST /api/resumes/parse
Body: { file_id: 123 }
```

---

## 📊 Success Criteria

**Phase 7A (Email UI):**
- ✅ Email templates display and can be edited
- ✅ Emails can be sent to recipients
- ✅ Email queue shows pending emails with auto-refresh
- ✅ Email history is searchable and filterable
- ✅ All success/error messages display clearly

**Phase 7B (Resume Upload UI):**
- ✅ Drag-and-drop upload works smoothly
- ✅ File validation prevents invalid uploads
- ✅ Progress bar displays during upload
- ✅ Parsed resume data displays correctly
- ✅ Resume selection works in job applications
- ✅ Admin can view all user resumes

---

## ⏱️ Time Estimates

| Component | Time | Priority |
|-----------|------|----------|
| Email Templates Manager | 1.5 hrs | HIGH |
| Email Sending Interface | 1 hr | HIGH |
| Email Queue Monitor | 1.5 hrs | HIGH |
| Email History | 1.5 hrs | MEDIUM |
| Resume Drag-Drop Upload | 2 hrs | HIGH |
| Resume Parser Display | 1.5 hrs | HIGH |
| Resume in Job Application | 1 hr | HIGH |
| Admin Resume Management | 1.5 hrs | MEDIUM |

**Total: ~12 hours**

---

## 🚀 Next Steps

1. ✅ **Complete Email UI Components** (4.5 hours)
2. ✅ **Complete Resume Upload UI** (6 hours)
3. ✅ **Integration Testing** (1-2 hours)
4. ✅ **Bug Fixes & Polish** (0.5-1 hour)

---

## 📝 Implementation Notes

- All components should use existing Bootstrap classes
- Follow current code organization pattern
- Add data-testid attributes for automation testing
- Include inline comments for complex logic
- Test each component with real API calls
- Ensure mobile responsiveness
- Add loading states for async operations
- Implement error handling with user-friendly messages

---

**Document Version:** 1.0  
**Last Updated:** October 27, 2025  
**Next Review:** After UI implementation
