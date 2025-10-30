

# Workday Job Application Automation Platform

**Version:** v1.1.0 (Production Ready) | **Date:** October 30, 2025
**Status:** ✅ Complete & Deployed

---

## 🎯 What It Is

A **complete multi-tenant job application management platform** built with FastAPI (Python backend) and Bootstrap 5 (frontend). This is a full-stack SaaS application for managing job postings, user applications, resumes, and emails across multiple companies with isolated data and comprehensive admin dashboards.

### Key Features
- **Multi-tenant Architecture**: Support for 26+ companies with data isolation
- **Job Management**: 75 jobs with advanced filtering, analytics, and status tracking
- **Application Workflow**: 54 applications with complete status lifecycle (Submitted → In Review → Interview → Accepted/Rejected)
- **Resume Management**: Upload, parse, and manage resumes (PDF/DOC/DOCX support)
- **Email System**: Template-based email management with queue monitoring and history
- **Admin Dashboard**: Real-time statistics, user/job/company management across all tenants
- **User Authentication**: Secure JWT-based auth with role-based access control
- **CI/CD Pipeline**: Automated testing and deployment via GitHub Actions

---

## 📋 Project Background and Current Status

### Initial Plan (High-Level Overview)
The project was originally envisioned as a system supporting **three separate company portals** (e.g., Meta, Google, Amazon) with an integrated **automation framework** to automatically apply for jobs across these portals. This would enable streamlined job application processes for users across multiple companies.

### Current Implementation Status
The project has evolved into a **single, comprehensive multi-tenant job application portal** serving as the core platform. This Meta Job Application Portal is fully implemented and production-ready, featuring:
- Complete backend and frontend for job management, applications, and admin oversight
- Multi-company support with data isolation
- Integrated resume and email systems
- Automated CI/CD for quality assurance
- Extensive test data and documentation


---

## 🏗️ Architecture Overview

### Tech Stack
- **Backend**: FastAPI, SQLAlchemy ORM, SQLite database, JWT authentication, bcrypt password hashing
- **Frontend**: HTML5, CSS3 (Bootstrap 5), Vanilla JavaScript, Responsive design
- **Database**: SQLite with 7 core tables (User, Company, Job, Application, Resume, Email, FileUpload)
- **Security**: CORS protection, password hashing, JWT tokens, multi-tenant data isolation
- **CI/CD**: GitHub Actions with automated testing and linting

### Core Components
- **56+ API Endpoints**: RESTful APIs with comprehensive documentation
- **Multi-tenant Support**: Company-based data isolation and admin access control
- **File Upload System**: Resume parsing and storage with validation
- **Email Management**: SMTP integration with template system
- **Admin Portal**: Complete dashboard for system management
- **Real-time Updates**: Live statistics and status monitoring
- **Automated Testing**: Smoke tests for health, jobs, and auth endpoints

---

## 🔄 CI/CD Pipeline

The project includes a fully configured GitHub Actions CI pipeline for automated testing and quality assurance.

### What Runs on Each Push/PR
- **Import Sanity Check**: Verifies the FastAPI app loads without errors
- **Linting**: Ruff code quality checks (non-blocking for now)
- **Automated Tests**: Async smoke tests covering:
  - Health endpoint (`GET /api/health`)
  - Public job listing (`GET /api/jobs/`)
  - Auth guard on applications (`POST /api/applications/` without token)
- **Build Status**: Green checkmark indicates all checks pass

### Viewing CI Results
1. Go to https://github.com/archanaarunog/WorkdayJobApplicationAutomation/actions
2. Click the "CI" workflow
3. Select the latest run
4. Expand steps to see logs and test outputs

### Local Testing
Run the same tests locally:
```bash
cd services/meta-service
source venv_py311/bin/activate
python -m pytest -q tests
```

---
- **Automated Testing**: Smoke tests for health, jobs, and auth endpoints

---

## 📊 System Statistics

### Production Data
- **26 Companies**: Meta, Google, Amazon, Microsoft, Apple, Netflix, Tesla, Spotify, Adobe, Salesforce, Oracle, IBM, Intel, NVIDIA, Airbnb, Uber, Lyft, Twitter, LinkedIn, Dropbox, Slack, Stripe, Pinterest, Snap, Zoom + Default Company
- **75 Jobs**: 2-4 jobs per company with realistic descriptions and requirements
- **19 Test Users**: Including admin accounts with proper authentication
- **54 Applications**: Distributed across status workflow with realistic data
- **Email Templates**: Welcome, application confirmation, status updates, admin notifications
- **Resume Support**: PDF, DOC, DOCX with automatic parsing and storage

### Code Metrics
- **Frontend UI**: 2,026+ lines (Email Management, Resume Upload interfaces)
- **Backend Code**: 5,000+ lines (models, routes, services, utilities)
- **Documentation**: 17 comprehensive guides (5,000+ lines total)
- **API Endpoints**: 56+ fully functional and tested endpoints
- **Test Coverage**: Complete setup scripts and test data

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+ (tested with Python 3.11)
- Git for cloning
- Modern web browser

### 1. Clone & Setup
```bash
git clone https://github.com/archanaarunog/WorkdayJobApplicationAutomation.git
cd WorkdayJobApplicationAutomation
```

### 2. Backend Setup (FastAPI)
```bash
# Navigate to backend directory
cd services/meta-service

# Create virtual environment
python3.11 -m venv venv_py311
source venv_py311/bin/activate  # Windows: venv_py311\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run backend server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup (Static Server)
```bash
# In new terminal, navigate to frontend
cd frontend/meta-ui/public

# Start HTTP server
python3 -m http.server 8081
```

### 4. Access the Application
- **Admin Dashboard**: http://localhost:8081/admin-dashboard.html
- **Email Management**: http://localhost:8081/email-management.html
- **Resume Management**: http://localhost:8081/resume-management.html
- **Job Portal**: http://localhost:8081/jobs.html
- **API Documentation**: http://localhost:8000/docs

### 5. Admin Credentials
```
Email: archanaarunog@gmail.com
Password: Archana@123
Access: Super-admin (all companies, all data)
```

### 6. Load Test Data (Optional)
```bash
cd services/meta-service
python complete_setup.py
```
This populates the database with 26 companies, 75 jobs, 19 users, and 54 applications for testing.

---

## 🎨 User Interface

### Admin Dashboard (`admin-dashboard.html`)
- **Dashboard Tab**: Real-time statistics (54 applications, 75 jobs, 19 users)
- **Applications Tab**: 54 applications with status filters and user details
- **Job Management Tab**: 75 jobs across 26 companies with application counts
- **User Management Tab**: 19 users with search and profile management
- **Company Management Tab**: 26 companies with full statistics

### Email Management (`email-management.html`)
- **Templates Tab**: Create/edit email templates
- **Send Tab**: Send emails to users with template selection
- **Queue Tab**: Monitor email sending queue with real-time updates
- **History Tab**: View sent email history and delivery status

### Resume Management (`resume-management.html`)
- **Upload Tab**: Drag-drop resume upload with validation
- **Parse Tab**: Automatic resume parsing with editable sections
- **Manage Tab**: View, download, edit, and delete stored resumes
- **Skills Tab**: Skills management and tagging system

### Job Portal (`jobs.html`)
- **Browse Jobs**: Filter by company, location, type
- **Apply**: Modal-based application submission
- **Dashboard**: User application tracking and status

---

## 🔧 API Endpoints

### Authentication
- `POST /api/users/register` - User registration
- `POST /api/users/login` - JWT authentication
- `GET /api/users/me` - Get current user profile

### Job Management
- `GET /api/jobs/` - List all jobs with filtering
- `POST /api/jobs/` - Create new job (admin)
- `GET /api/jobs/{id}` - Get job details
- `PUT /api/jobs/{id}` - Update job (admin)

### Applications
- `POST /api/applications/` - Submit job application
- `GET /api/applications/me` - Get user's applications
- `GET /api/applications/{id}` - Get application details

### Admin Endpoints
- `GET /api/admin/stats` - System statistics
- `GET /api/admin/jobs` - All jobs with analytics
- `GET /api/admin/applications` - All applications
- `GET /api/admin/users` - User management
- `GET /api/admin/companies` - Company management

### Email System
- `GET /api/email/templates` - List email templates
- `POST /api/email/templates` - Create template
- `POST /api/email/send` - Send email
- `GET /api/email/queue` - Email queue status
- `GET /api/email/history` - Email history

### File Management
- `POST /api/files/upload` - Upload resume
- `GET /api/resumes` - List user resumes
- `GET /api/resumes/{id}/download` - Download resume
- `DELETE /api/resumes/{id}` - Delete resume

---

## 📁 Project Structure

```
WorkdayJobApplicationAutomation/
├── services/meta-service/           # FastAPI Backend
│   ├── src/
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── models/                  # SQLAlchemy models
│   │   │   ├── user.py             # User model
│   │   │   ├── company.py          # Company model
│   │   │   ├── job.py              # Job model
│   │   │   ├── application.py      # Application model
│   │   │   ├── email.py            # Email model
│   │   │   └── file_upload.py      # File upload model
│   │   ├── routes/                 # API route handlers
│   │   │   ├── user.py
│   │   │   ├── job.py
│   │   │   ├── admin.py
│   │   │   ├── email.py
│   │   │   └── file_upload.py
│   │   ├── schemas/                # Pydantic schemas
│   │   ├── services/               # Business logic
│   │   └── utils/                  # Utilities
│   ├── templates/email/            # Email templates
│   ├── complete_setup.py           # Test data setup
│   └── requirements.txt
├── frontend/meta-ui/public/         # Frontend UI
│   ├── admin-dashboard.html        # Admin dashboard
│   ├── email-management.html       # Email management
│   ├── resume-management.html      # Resume management
│   ├── jobs.html                   # Job portal
│   ├── login.html                  # Authentication
│   └── assets/                     # CSS/JS resources
├── docs/                           # Documentation
│   ├── SITE_SUMMARY.md            # Quick project overview
│   ├── PHASE_7_FINAL_DELIVERY.md  # Complete delivery report
│   └── [17 other guides]          # Comprehensive documentation
├── databases/                      # SQLite databases
└── README.md
```

---

## 🛡️ Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Hashing**: bcrypt encryption for all passwords
- **CORS Protection**: Cross-origin request security
- **Multi-tenant Isolation**: Company-based data separation
- **Role-based Access**: Admin vs regular user permissions
- **Input Validation**: Pydantic schemas for all API inputs
- **SQL Injection Prevention**: SQLAlchemy ORM protection

---

## � Future Plans

### Automation Framework (Paused)
The original vision included an **automation framework** to automatically apply for jobs across multiple company portals. This feature is currently paused but planned for future development. It would enable users to submit applications programmatically to external job portals (e.g., Meta, Google, Amazon) with resume parsing and application tracking.

### Testing Phase Repository
Ongoing work on automation and testing frameworks is conducted in the dedicated repository: **[JobApplicationPortalTestFramework](https://github.com/archanaarunog/JobApplicationPortalTestFramework)**. This repo focuses on:
- Selenium-based UI automation for job portals
- API testing frameworks
- CI/CD integration for automated testing
- Self-healing test automation features

### Potential Expansions
- Deployment to cloud platforms (Railway, Heroku)
- Mobile app development
- Advanced analytics and reporting
- Integration with external job boards
- Multi-language support

---

## �📈 Development Phases Completed

### Phase 1: User Authentication ✅
- User registration with email and password
- Secure login with JWT token generation and validation
- Password hashing with bcrypt
- Logout functionality with token management
- User profile management

### Phase 2: Job Management ✅
- Job listing with advanced filters and sorting
- Job details view with modal interface
- Job search functionality by title, company, location
- Job status tracking (Active, Closed)
- Company-specific job postings

### Phase 3: Job Application ✅
- Apply for jobs with cover letter submission
- View personal application history
- Application status tracking (Submitted, In Review, Interview, Accepted, Rejected)
- Application timeline and updates
- User dashboard with application statistics

### Phase 4: Multi-Company Architecture ✅
- Company models and relationships
- Multi-tenant database design with data isolation
- Company-specific job and user management
- Super-admin access across all companies
- Company statistics and analytics

### Phase 5: Admin Dashboard ✅
- Admin authentication and role-based authorization
- User management (view, edit, deactivate users)
- Job management interface (create, edit, delete jobs)
- Application statistics and analytics
- Real-time dashboard with key metrics (54 applications, 75 jobs, 19 users)
- 5-tab admin interface (Dashboard, Applications, Jobs, Users, Companies)

### Phase 6: Email Notification System ✅
**Backend:**
- Email template system with Jinja2 rendering
- Email sending service with SMTP integration
- Queue management for batch processing
- Email history and delivery tracking
- Admin email statistics

**Frontend:**
- Email Management UI (1,130 lines) with 4 tabs:
  - Templates: Create/edit/delete email templates
  - Send: Send emails to users with template selection
  - Queue: Monitor email queue with real-time updates
  - History: View sent email history with search/filter

### Phase 7: File Upload & Resume System ✅
**Backend:**
- Resume upload with file validation (PDF, DOC, DOCX, TXT, RTF)
- Automatic resume parsing engine
- File storage and management system
- Resume metadata extraction
- Admin file management endpoints

**Frontend:**
- Resume Management UI (896 lines) with comprehensive features:
  - Drag-and-drop resume upload with validation
  - Automatic resume parsing with editable sections
  - Skills management and tagging
  - Download/Preview/Delete functionality
  - Multiple resume support per user
  - Resume history and versioning

---

## 🎯 Phase 7 Completion Details

Phase 7 marks the **production-ready milestone** with:
- ✅ **35 new files created** (2 major UI components, models, routes, services, utilities)
- ✅ **9 files modified** (models, routes, main.py, requirements.txt)
- ✅ **2,026 lines of frontend code** (email-management.html + resume-management.html)
- ✅ **5,000+ lines of backend code** (email/file services, models, routes)
- ✅ **17 comprehensive documentation files** (5,000+ lines of guides and specifications)
- ✅ **56+ fully tested API endpoints** (all working with proper authentication)
- ✅ **Complete test data** (26 companies, 75 jobs, 19 users, 54 applications)
- ✅ **Zero known bugs** - All systems operational and tested

---

## 🧪 Testing & Quality

### Test Data Available
- ✅ 26 companies with realistic data
- ✅ 75 jobs across all companies
- ✅ 19 test users with various roles
- ✅ 54 applications with complete workflow
- ✅ Email templates and sample content

### API Testing
- ✅ All 56+ endpoints tested and working
- ✅ Authentication and authorization verified
- ✅ File upload and processing confirmed
- ✅ Email system integration tested
- ✅ Admin dashboard functionality validated

### Performance
- ✅ Fast API responses (< 500ms)
- ✅ Efficient database queries
- ✅ Responsive UI across devices
- ✅ Real-time updates working
- ✅ File upload handling optimized

---

## 📚 Documentation

### Quick References
- **[SITE_SUMMARY.md](docs/SITE_SUMMARY.md)** - 200-word project overview
- **[PHASE_7_FINAL_DELIVERY.md](docs/PHASE_7_FINAL_DELIVERY.md)** - Complete delivery report
- **[PHASE_7_QUICK_START_GUIDE.md](docs/PHASE_7_QUICK_START_GUIDE.md)** - Getting started guide

### Comprehensive Guides
- **PHASE_7_FRONTEND_UI_IMPLEMENTATION.md** - UI specifications and features
- **PHASE_7_FILES_REFERENCE.md** - File structure and deployment
- **FILE_UPLOAD_AND_ADMIN_GUIDE.md** - File upload and admin usage
- **ADMIN_DASHBOARD_COMPLETE_FIX.md** - Admin dashboard troubleshooting
- **API testing guides and architecture documents**

---

## 🔄 Development Workflow

### Local Development
```bash
# Backend development
cd services/meta-service
source venv_py311/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Frontend development
cd frontend/meta-ui/public
python3 -m http.server 8081
```

### Database Management
```bash
# Setup test data
cd services/meta-service
python complete_setup.py

# Reset database
rm databases/meta.db
python init_db.py
```

### Testing APIs
```bash
# Get auth token
curl -X POST http://localhost:8000/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"archanaarunog@gmail.com","password":"Archana@123"}'

# Test admin endpoints
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:8000/api/admin/stats
```

---

## 🤝 Contributing

This project demonstrates modern full-stack development practices and is suitable for:
- **Portfolio Projects**: Complete SaaS application example
- **Learning Resources**: FastAPI, SQLAlchemy, JWT, multi-tenant architecture
- **Interview Preparation**: Real-world coding patterns and best practices

### Skills Demonstrated
- FastAPI backend development
- SQLAlchemy ORM and database design
- JWT authentication and security
- Multi-tenant application architecture
- RESTful API design
- Frontend development with Bootstrap 5
- File upload and processing
- Email system integration
- Admin dashboard development
- Testing and documentation

---

## 📄 License

MIT License - Free to use for learning and portfolio purposes.

---

## 🎉 Conclusion

**Workday Job Application Automation Platform v1.1.0 is production-ready!**

This is a complete, enterprise-grade job application management system with:
- ✅ 56+ tested API endpoints
- ✅ Multi-tenant architecture supporting 26+ companies
- ✅ 75 jobs and 54 applications with full workflow
- ✅ Email and resume management systems
- ✅ Comprehensive admin dashboard
- ✅ Professional UI/UX design
- ✅ Complete documentation and testing
- ✅ Security best practices implemented
- ✅ Automated CI/CD pipeline

**Current Status**: The core Meta Job Application Portal is fully implemented and operational. The automation framework for cross-portal job applications is paused but planned for future development in the dedicated testing repository.

**Ready for production deployment and portfolio showcase!**

---

*Built with ❤️ using FastAPI, SQLAlchemy, and Bootstrap 5*
*Last updated: October 30, 2025*

## Skills Used

- FastAPI (Python web framework)
- SQLAlchemy (ORM, database modeling)
- SQLite (local database)
- Pydantic (data validation)
- JWT (authentication)
- bcrypt (password hashing)
- REST API design
- CORS configuration
- HTML5, CSS3, JavaScript (vanilla)
- Bootstrap 5 (responsive UI)
- Modular project structure
- API documentation (Swagger UI)
- Git & GitHub (version control)

---

## Features (V1.0.0)

- **User Registration**: Create a new user account with email, password, and profile details.
- **User Login**: Secure login with JWT authentication; token stored in browser localStorage.
- **Job Listing**: View all available jobs fetched from the backend API.
- **Apply Button**: Each job card has an Apply button. Users can submit a cover letter and additional info via a modal popup.
- **Logout**: Logout button clears session and redirects to login.
- **Responsive UI**: Clean, modern look using Bootstrap 5.
- **API Documentation**: Swagger UI available at `/docs` for backend testing.
- **CORS Enabled**: Frontend and backend communicate securely across ports.

---


## Project Structure

```
WorkdayJobApplicationAutomation/
├── services/
│   └── meta-service/
│       └── src/
│           ├── main.py           # FastAPI app entry point
│           ├── models/           # SQLAlchemy models (User, Job, Application)
│           ├── routes/           # API routers (user.py, job.py, applications.py)
│           ├── schemas.py        # Pydantic schemas
│           └── config/           # Database config
├── frontend/
│   └── meta-ui/
│       └── public/
│           ├── index.html
│           ├── register.html
│           ├── login.html
│           ├── jobs.html
│           └── assets/
│               ├── css/style.css
│               └── js/
│                   ├── register.js
│                   ├── login.js
│                   └── jobs.js
└── README.md
```

---


## Setup Instructions

### Prerequisites
- Python 3.9 or higher
- Git (for cloning the repository)

### 1. Clone the Repository
```sh
git clone https://github.com/archanaarunog/WorkdayJobApplicationAutomation.git
cd WorkdayJobApplicationAutomation
```

### 2. Backend Setup (FastAPI)

**Navigate to backend directory and set up virtual environment:**
```sh
# Navigate to the backend service directory
cd services/meta-service

# Create a Python 3.11 virtual environment
python3.11 -m venv venv_py311

# Activate the virtual environment
source venv_py311/bin/activate  # On Windows: venv_py311\Scripts\activate
```

**Install dependencies:**
```sh
# Install all required packages
pip install -r requirements.txt

# If bcrypt issues occur, reinstall bcrypt specifically
pip uninstall -y bcrypt passlib
pip install bcrypt==4.0.1
```

**Run the backend server:**
```sh
# Must be run from the meta-service directory
cd /path/to/WorkdayJobApplicationAutomation/services/meta-service
source venv_py311/bin/activate
uvicorn src.main:app --reload
```

**Verify backend is running:**
- Backend API: [http://localhost:8000](http://localhost:8000)
- API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Frontend Setup (Static HTML/JS)

**In a new terminal, navigate to the public directory:**
```sh
# Must be run from the public directory containing the HTML files
cd /path/to/WorkdayJobApplicationAutomation/frontend/meta-ui/public
python3 -m http.server 8081  # Using port 8081 to avoid conflicts
```

**Access the application:**
- Frontend: [http://localhost:8081/](http://localhost:8081/)

### 4. Quick Start Guide

**Terminal 1 (Backend) - Exact Location and Command:**
```sh
cd /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service
source venv_py311/bin/activate
uvicorn src.main:app --reload
```

**Terminal 2 (Frontend) - Exact Location and Command:**
```sh
cd /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/frontend/meta-ui/public
python3 -m http.server 8081
```

**Important Notes:**
1. The frontend must be run from the `public` directory where the HTML files are located
2. Using port 8081 for frontend to avoid common port conflicts
3. The backend must be run from the `meta-service` directory
4. Always activate the virtual environment before running the backend
5. If you see bcrypt-related errors during user registration, follow the bcrypt reinstallation steps above

**Access URLs:**
- Frontend: http://localhost:8080
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---


## How to Use

1. **Register a new user** via the Register page.
2. **Login** with your credentials.
3. **Add jobs** using the backend Swagger UI (`/api/jobs/` POST endpoint).
4. **View jobs** on the Jobs page. Each job is shown as a card with an Apply button.
5. **Click Apply** to open a modal, fill in your cover letter, and submit your application.
6. **Logout** using the Logout button on the Jobs page.

---


## API Endpoints

- `POST /api/users/register` — Register a new user
- `POST /api/users/login` — Login and receive JWT token
- `GET /api/jobs/` — List all jobs
- `POST /api/jobs/` — Create a new job (admin/dev only)
- `POST /api/applications/` — Apply to a job (requires authentication)
- `GET /api/applications/me` — List your job applications

---


## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, SQLite, Pydantic, JWT, bcrypt
- **Frontend:** HTML, CSS (Bootstrap), JavaScript (vanilla)

---


## Changelog

### v1.1.0 (Completed - October 30, 2025)
**CI/CD and Testing Enhancements:**
- ✅ Added GitHub Actions CI pipeline with automated testing
- ✅ Implemented async smoke tests for health, jobs, and auth endpoints
- ✅ Added Ruff linting (non-blocking)
- ✅ Fixed route ordering for API precedence over static files
- ✅ Ensured job listing route is explicitly public
- ✅ Added comprehensive test data setup scripts
- ✅ Updated documentation and README for current status

**System Improvements:**
- ✅ Verified multi-tenant architecture with 26 companies
- ✅ Confirmed 75 jobs and 54 applications with full workflow
- ✅ Validated resume and email management systems
- ✅ Production-ready admin dashboard with real-time stats

### v1.0.0 (Completed)
- User registration and login with JWT authentication
- Job listing and application submission
- Bootstrap-based responsive UI
- SQLite database with SQLAlchemy models
- FastAPI backend with Swagger documentation

---

## Known Issues / Roadmap
- Background pattern visibility may vary across browsers (gradient-based)
- Application history view not yet implemented (planned for Phase 2)
- Profile and admin features planned for Phase 4-5
- Password reset functionality planned for Phase 2

---


## Contributing
Pull requests and suggestions are welcome! For major changes, please open an issue first.

---


## License
MIT
