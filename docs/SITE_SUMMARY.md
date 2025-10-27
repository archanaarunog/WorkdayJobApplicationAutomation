# Workday Job Application Automation - Site Summary

## What It Is
A **complete job application management platform** built with FastAPI (Python backend) and Bootstrap 5 (frontend). It's a full-stack SaaS application for managing job postings, user applications, resumes, and emails across multiple companies.

## Core Features
- **Multi-tenant system** supporting 26+ companies with isolated data
- **Job management**: 75 jobs with advanced filtering and analytics
- **User accounts**: 19 test users with secure JWT authentication
- **Application tracking**: 54 job applications with status workflow (Submitted → In Review → Interview → Accepted/Rejected)
- **Resume management**: Upload, parse, and store resumes (PDF/DOC/DOCX support)
- **Email system**: Send templated emails, manage queues, track history
- **Admin dashboard**: Real-time statistics, user/job/company management

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, SQLite, JWT authentication, bcrypt
- **Frontend**: HTML5, CSS3 (Bootstrap 5), Vanilla JavaScript
- **Database**: SQLite with 7 core tables (User, Company, Job, Application, Resume, Email, FileUpload)

## Key Pages
- Admin Dashboard (statistics, job/user/application management)
- Email Management (template CRUD, send, queue monitoring)
- Resume Management (drag-drop upload, parsing, download)
- Job Portal (listing, search, apply)
- User Auth (register, login, profile)

## Production Ready
✅ All APIs tested and working | ✅ 56+ endpoints | ✅ Responsive UI | ✅ Multi-company support | ✅ Security implemented (CORS, password hashing, JWT) | ✅ Error handling complete | ✅ Documentation comprehensive

## Quick Start
```bash
# Backend (Terminal 1)
cd services/meta-service && source venv_py311/bin/activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Frontend (Terminal 2)
cd frontend/meta-ui/public && python3 -m http.server 8081

# Access: http://localhost:8081/admin-dashboard.html (archanaarunog@gmail.com / Archana@123)
```

**Status**: ✅ Phase 7 Complete - Production Ready (v1.1.0)
