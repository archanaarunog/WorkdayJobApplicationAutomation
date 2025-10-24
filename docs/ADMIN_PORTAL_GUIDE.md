# Admin Portal - Complete Guide

## 🎯 Overview

The Admin Portal is a separate administrative interface that allows authorized users to manage job applications, view analytics, and control the job portal system. It provides a centralized dashboard for HR teams and administrators to oversee the entire recruitment process.

---

## 🚀 Current Features (Phase 4 - Completed)

### ✅ **Admin Dashboard**
- **Statistics Overview**: 4 key metrics cards
  - Total Applications (all submitted applications)
  - Active Jobs (currently open positions)
  - Total Users (registered candidates)
  - Interviews (applications in interview stage)

### ✅ **Application Management**
- **View All Applications**: Complete table with candidate and job details
- **Status Filtering**: Filter by application status
  - All, Submitted, In Review, Interview, Accepted, Rejected
- **Status Updates**: Change application status via dropdown menu
- **Candidate Information**: Name, email, phone number
- **Job Details**: Title, company, department, location
- **Applied Date**: When candidate submitted application

### ✅ **Admin Authentication**
- **Role-based Access Control**: Only users with `is_admin = True` can access
- **Secure API Endpoints**: All admin routes require admin privileges
- **Session Management**: Uses same JWT token system with admin role validation

---

## 👤 Admin Account Creation

### Method 1: Script-based (Current Implementation)
**Steps:**
1. **Start Backend Server**
   ```bash
   cd /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service
   source venv_py311/bin/activate
   uvicorn src.main:app --reload
   ```

2. **Register Regular Account First**
   - Go to `http://localhost:8081/register.html`
   - Create account with your email (e.g., `admin@company.com`)
   - Complete registration process

3. **Run Admin Script**
   ```bash
   cd services/meta-service
   source venv_py311/bin/activate
   python make_admin.py your@email.com
   ```

4. **Access Admin Dashboard**
   - Go to `http://localhost:8081/admin-dashboard.html`
   - Login with your admin credentials
   - You'll now have admin access

### Method 2: Admin Registration Page (Recommended for Production)

**To Implement:**
Create a separate admin registration page with:
- Admin-specific registration form
- Company association
- Admin verification process
- Email confirmation

---

## 🏢 Multi-Company Architecture

### Current Implementation (Single Company)
- **Current State**: All jobs and applications are in one database
- **Admin Access**: Admin can see ALL applications across the entire system
- **No Company Filtering**: Admin sees everything regardless of company

### Recommended Multi-Company Setup

#### **Database Schema Changes**
```sql
-- Add company table
CREATE TABLE companies (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Add company_id to users table
ALTER TABLE users ADD COLUMN company_id INTEGER REFERENCES companies(id);

-- Add company_id to jobs table  
ALTER TABLE jobs ADD COLUMN company_id INTEGER REFERENCES companies(id);

-- Add company_id to admin users
ALTER TABLE users ADD COLUMN admin_company_id INTEGER REFERENCES companies(id);
```

#### **How Multi-Company Would Work**
1. **Company Registration**
   - Companies register first: "Meta", "Google", "Amazon"
   - Each gets unique company ID

2. **User Registration**
   - Users register with company email domain
   - System auto-assigns company based on email domain
   - `john@meta.com` → Meta company
   - `sarah@google.com` → Google company

3. **Admin Accounts**
   - Admins are associated with specific companies
   - `hr@meta.com` admin can only see Meta applications
   - `recruiter@google.com` admin can only see Google applications

4. **Data Filtering**
   - Jobs: Only show jobs from admin's company
   - Applications: Only show applications to admin's company jobs
   - Users: Only show candidates who applied to admin's company

---

## 🎛️ Admin Portal Features

### **Current Features (Implemented)**

#### **1. Dashboard Statistics**
```javascript
// What admin sees:
{
  "total_applications": 25,    // All applications in system
  "total_jobs": 8,            // All active jobs
  "total_users": 15,          // All registered candidates  
  "by_status": {
    "submitted": 10,
    "in_review": 8,
    "interview": 4,
    "accepted": 2,
    "rejected": 1
  }
}
```

#### **2. Application Management**
- **View Applications**: Table with all application details
- **Filter by Status**: Dropdown filters for each status
- **Update Status**: Change application status with dropdown
- **Candidate Details**: Name, email, contact information
- **Job Information**: Title, company, department

#### **3. Access Control**
- **Authentication**: JWT token with admin role check
- **Authorization**: Backend validates admin status on every request
- **Redirect**: Non-admin users redirected to regular jobs page

---

### **Planned Features (Next Phases)**

#### **Phase 5.1: Job Management** 
- **Create Jobs**: Admin form to post new jobs
- **Edit Jobs**: Modify existing job postings
- **Delete Jobs**: Remove job postings (with confirmation)
- **Job Status**: Activate/deactivate job listings

#### **Phase 5.2: User Management**
- **View All Users**: Table of all registered candidates
- **User Details**: Full profile information
- **Account Actions**: Disable/enable user accounts
- **User Statistics**: Registration trends, activity

#### **Phase 5.3: Advanced Analytics**
- **Charts & Graphs**: Visual analytics dashboard
- **Application Trends**: Applications over time
- **Job Performance**: Which jobs get most applications
- **Conversion Rates**: Application → Interview → Hire rates

#### **Phase 5.4: Company Management** (Multi-tenant)
- **Company Settings**: Configure company profile
- **Domain Management**: Manage allowed email domains
- **Admin Permissions**: Manage admin access levels
- **Company Analytics**: Company-specific metrics

---

## 🔧 API Endpoints (Admin)

### **Authentication Required**
All admin endpoints require:
```http
Authorization: Bearer <jwt_token>
```
And user must have `is_admin = true`

### **Current Endpoints**

#### **Get Admin Statistics**
```http
GET /api/admin/stats
Response: {
  "total_applications": 25,
  "total_jobs": 8, 
  "total_users": 15,
  "by_status": { ... }
}
```

#### **Get All Applications**
```http
GET /api/admin/applications
GET /api/admin/applications?status=submitted
Response: [
  {
    "id": 1,
    "status": "submitted",
    "applied_at": "2025-10-24T10:30:00Z",
    "user": { "name": "John Doe", "email": "john@email.com" },
    "job": { "title": "Software Engineer", "company": "Meta" }
  }
]
```

#### **Update Application Status**
```http
PATCH /api/admin/applications/{id}/status
Body: { "status": "in_review" }
Response: { "message": "Status updated", "status": "in_review" }
```

---

## 📊 Current Test Data (Phase 4 Complete)

### **Database Overview**
After running the complete setup, your system contains:

#### **👥 Sample Users (5 users)**
```
1. john.doe@gmail.com     | Password: password123 | John Doe
2. jane.smith@gmail.com   | Password: password123 | Jane Smith  
3. mike.johnson@gmail.com | Password: password123 | Mike Johnson
4. sarah.wilson@gmail.com | Password: password123 | Sarah Wilson
5. alex.brown@gmail.com   | Password: password123 | Alex Brown
```

#### **💼 Sample Jobs (25 jobs)**
```
Companies: Meta, Google, Amazon, Microsoft, Apple, Netflix, Tesla, etc.
Positions: Software Engineer, Senior Developer, QA Engineer, Product Manager
Locations: San Francisco, Austin, New York, Seattle, Portland
Salaries: $57k - $217k range
Departments: Engineering, Product, QA, Security, etc.
```

#### **📋 Sample Applications (13 applications)**
```
Status Breakdown:
- Submitted: 7 applications
- In Review: 2 applications  
- Interview: 1 application
- Accepted: 2 applications
- Rejected: 1 application

Sample Applications:
- John → QA Engineer at Airbnb (Submitted)
- Jane → Senior Software Engineer at Google (Submitted)
- Mike → Technical Lead at LinkedIn (In Review)  
- Sarah → Software Engineer at Meta (Submitted)
- Alex → Product Manager at Adobe (Submitted)
- ... and 8 more applications
```

### **Admin Account**
```
Admin User: archanaarunog@gmail.com (your account)
Admin Status: ✅ Active (set via make_admin.py script)
Admin Access: Full system access to all companies/applications
```

---

## 🧪 Testing Admin Features

### **Step 1: Setup**
```bash
# Terminal 1 - Backend  
cd services/meta-service
source venv_py311/bin/activate
uvicorn src.main:app --reload

# Terminal 2 - Frontend
cd frontend/meta-ui/public
python3 -m http.server 8081
```

### **Step 2: Access Admin Dashboard**
```bash
# Test data already created! Just access:
# URL: http://localhost:8081/admin-dashboard.html
# Login: archanaarunog@gmail.com (your admin account)
```

### **Step 3: Test Admin Flow**
1. **Register as regular user** at `http://localhost:8081/register.html`
2. **Apply to some jobs** at `http://localhost:8081/jobs.html`
3. **Make yourself admin**: `python make_admin.py your@email.com`
4. **Access admin dashboard** at `http://localhost:8081/admin-dashboard.html`
5. **Test all features**:
   - View statistics (should show numbers > 0)
   - Filter applications by status
   - Change application status
   - Verify updates reflect in statistics

---

## 🏗️ Implementation Architecture

### **Frontend Structure**
```
frontend/meta-ui/public/
├── admin-dashboard.html     # Admin dashboard page
├── assets/js/
│   └── admin-dashboard.js   # Admin functionality
└── assets/css/
    └── admin-styles.css     # Admin-specific styles
```

### **Backend Structure**
```
services/meta-service/src/
├── routes/
│   └── admin.py            # Admin API endpoints
├── models/
│   └── user.py             # User model with is_admin field
└── make_admin.py           # Script to grant admin privileges
```

### **Database Schema**
```sql
-- Users table with admin flag
users (
  id, email, password_hash, first_name, last_name, phone,
  is_admin BOOLEAN DEFAULT FALSE,  -- Admin privilege flag
  created_at, updated_at
)

-- Applications with status tracking
applications (
  id, user_id, job_id, cover_letter, resume_url,
  status ENUM('submitted', 'in_review', 'interview', 'accepted', 'rejected'),
  applied_at, updated_at
)
```

---

## 🚀 Future Enhancements

### **Phase 5: Advanced Admin Features**
1. **Job CRUD Operations**
   - Full job management interface
   - Bulk job operations
   - Job templates

2. **Advanced Filtering**
   - Date range filters
   - Department-specific views
   - Custom search queries

3. **Bulk Actions**
   - Bulk status updates
   - Export applications to CSV
   - Batch email notifications

4. **Real-time Updates**
   - WebSocket connections
   - Live application notifications
   - Real-time statistics

### **Phase 6: Multi-Company Support**
1. **Company Management**
   - Company registration system
   - Domain-based user assignment
   - Company-specific branding

2. **Advanced Admin Roles**
   - Super Admin (cross-company access)
   - Company Admin (company-specific)
   - Department Admin (department-specific)

3. **Data Isolation**
   - Company-specific data filtering
   - Secure multi-tenancy
   - Company analytics

---

## 📊 Admin Portal Success Metrics

### **Phase 4 Completed ✅**
- ✅ Admin authentication working
- ✅ Dashboard statistics displaying
- ✅ Application table with filtering
- ✅ Status update functionality
- ✅ Role-based access control

### **Ready for Phase 5**
Now that admin basics are working, you're ready to add:
- Job management (create/edit/delete jobs)
- User management (view/manage candidates)
- Advanced analytics (charts and reports)

---

## 🎯 Next Steps

1. **Test Current Features**: Verify all admin functionality works as expected
2. **Create Test Data**: Add sample jobs and applications for testing
3. **Phase 5.1**: Implement job management features
4. **Phase 5.2**: Add user management capabilities
5. **Phase 6**: Consider multi-company architecture if needed

**Current Status: ✅ Phase 4 Complete - Admin Dashboard Functional**

The admin portal is now fully operational and ready for additional features!