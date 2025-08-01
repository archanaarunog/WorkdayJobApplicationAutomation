# API Specifications - JAPS

## Overview
This document defines all REST API endpoints for the Job Application Portal System (JAPS). Each portal exposes its own set of APIs with consistent patterns and authentication mechanisms.

---

## 1. JAPS Main Portal APIs

**Base URL:** `http://localhost:3000/api`

### Job Aggregation Endpoints

#### GET /companies
Get list of all registered company portals.

**Response:**
```json
{
  "companies": [
    {
      "id": 1,
      "name": "Meta",
      "portal_url": "http://localhost:3001",
      "status": "active"
    }
  ]
}
```

#### GET /jobs
Get aggregated job listings from all portals.

**Query Parameters:**
- `search` (string): Search term for job title/description
- `location` (string): Filter by location
- `company` (string): Filter by company name
- `limit` (integer): Number of results (default: 50)
- `offset` (integer): Pagination offset (default: 0)

**Response:**
```json
{
  "jobs": [
    {
      "id": 1,
      "title": "Software Engineer",
      "company": "Meta",
      "location": "Menlo Park, CA",
      "salary_range": "$120,000 - $180,000",
      "job_type": "Full-time",
      "experience_level": "Mid-level",
      "portal_url": "http://localhost:3001/apply?job_id=1",
      "last_synced": "2025-08-01T10:30:00Z"
    }
  ],
  "total": 25,
  "limit": 50,
  "offset": 0
}
```

#### POST /sync-jobs
Trigger job sync from all company portals (admin endpoint).

**Response:**
```json
{
  "message": "Job sync initiated",
  "sync_id": "sync_123456789"
}
```

#### GET /sync-status/{sync_id}
Check status of job synchronization.

**Response:**
```json
{
  "sync_id": "sync_123456789",
  "status": "completed",
  "companies_synced": 3,
  "total_jobs_fetched": 45,
  "completed_at": "2025-08-01T10:35:00Z"
}
```

---

## 2. Meta Portal APIs

**Base URL:** `http://localhost:3001/api`

### Authentication Endpoints

#### POST /register
Register a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1-555-0123"
}
```

**Response (201):**
```json
{
  "message": "User registered successfully",
  "user_id": 123
}
```

**Error Response (400):**
```json
{
  "error": "Email already exists",
  "field": "email"
}
```

#### POST /login
Authenticate user and get session token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200):**
```json
{
  "token": "jwt_token_here",
  "user": {
    "id": 123,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "expires_at": "2025-08-02T10:30:00Z"
}
```

#### POST /logout
Invalidate current session token.

**Headers:** `Authorization: Bearer {token}`

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

### Job Endpoints

#### GET /jobs
Get Meta job listings.

**Query Parameters:**
- `search` (string): Search term
- `department` (string): Filter by department
- `location` (string): Filter by location
- `job_type` (string): Full-time, Part-time, Contract
- `limit` (integer): Results limit (default: 20)
- `offset` (integer): Pagination offset

**Response:**
```json
{
  "jobs": [
    {
      "id": 1,
      "title": "Software Engineer - Frontend",
      "department": "Engineering",
      "location": "Menlo Park, CA",
      "job_type": "Full-time",
      "experience_level": "Mid-level",
      "salary_min": 120000,
      "salary_max": 180000,
      "description": "Build the future of social technology...",
      "requirements": "3+ years of React experience...",
      "posted_date": "2025-07-28T00:00:00Z"
    }
  ],
  "total": 15
}
```

#### GET /jobs/{job_id}
Get specific job details.

**Response:**
```json
{
  "id": 1,
  "title": "Software Engineer - Frontend",
  "department": "Engineering",
  "location": "Menlo Park, CA",
  "job_type": "Full-time",
  "experience_level": "Mid-level",
  "salary_min": 120000,
  "salary_max": 180000,
  "description": "Detailed job description...",
  "requirements": "Detailed requirements...",
  "posted_date": "2025-07-28T00:00:00Z",
  "is_active": true
}
```

### Application Endpoints

#### POST /apply
Submit job application.

**Headers:** `Authorization: Bearer {token}`

**Request Body:**
```json
{
  "job_id": 1,
  "cover_letter": "I am excited to apply for this position...",
  "additional_info": "Additional information about my qualifications..."
}
```

**Response (201):**
```json
{
  "message": "Application submitted successfully",
  "application_id": 456,
  "status": "submitted"
}
```

#### GET /my-applications
Get user's applications.

**Headers:** `Authorization: Bearer {token}`

**Response:**
```json
{
  "applications": [
    {
      "id": 456,
      "job": {
        "id": 1,
        "title": "Software Engineer - Frontend",
        "department": "Engineering"
      },
      "status": "submitted",
      "applied_at": "2025-08-01T09:30:00Z"
    }
  ]
}
```

### Profile Endpoints

#### GET /profile
Get user profile.

**Headers:** `Authorization: Bearer {token}`

**Response:**
```json
{
  "id": 123,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1-555-0123",
  "created_at": "2025-07-30T12:00:00Z"
}
```

#### PUT /profile
Update user profile.

**Headers:** `Authorization: Bearer {token}`

**Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Smith",
  "phone": "+1-555-0124"
}
```

**Response (200):**
```json
{
  "message": "Profile updated successfully"
}
```

---

## 3. Amazon Portal APIs

**Base URL:** `http://localhost:3002/api`

### Extended Authentication (similar to Meta plus)

#### POST /register
Enhanced registration with additional fields.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1-555-0123",
  "address": "123 Main St",
  "city": "Seattle",
  "state": "WA",
  "zip_code": "98101",
  "linkedin_url": "https://linkedin.com/in/johndoe"
}
```

### Enhanced Application Endpoints

#### POST /apply
Extended application with Amazon-specific fields.

**Headers:** `Authorization: Bearer {token}`

**Request Body:**
```json
{
  "job_id": 1,
  "cover_letter": "Cover letter text...",
  "why_amazon": "Why I want to work at Amazon...",
  "availability_date": "2025-09-01",
  "willing_to_relocate": true,
  "salary_expectation": 150000
}
```

### Experience Management

#### POST /experience
Add work experience.

**Headers:** `Authorization: Bearer {token}`

**Request Body:**
```json
{
  "company_name": "Previous Company",
  "job_title": "Software Developer",
  "start_date": "2022-01-01",
  "end_date": "2024-12-31",
  "description": "Developed web applications...",
  "is_current": false
}
```

#### GET /experience
Get user's work experience.

**Headers:** `Authorization: Bearer {token}`

**Response:**
```json
{
  "experience": [
    {
      "id": 1,
      "company_name": "Previous Company",
      "job_title": "Software Developer",
      "start_date": "2022-01-01",
      "end_date": "2024-12-31",
      "description": "Developed web applications...",
      "is_current": false
    }
  ]
}
```

#### POST /education
Add education information.

**Headers:** `Authorization: Bearer {token}`

**Request Body:**
```json
{
  "school_name": "University of Washington",
  "degree": "Bachelor of Science",
  "field_of_study": "Computer Science",
  "graduation_year": 2022,
  "gpa": 3.75
}
```

---

## 4. Google Portal APIs

**Base URL:** `http://localhost:3003/api`

### Advanced Features

#### POST /register
Registration with Google-specific fields.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1-555-0123",
  "github_url": "https://github.com/johndoe",
  "portfolio_url": "https://johndoe.dev",
  "preferred_pronouns": "he/him",
  "diversity_info": "Optional diversity information..."
}
```

### Resume Management

#### POST /resume/upload
Upload resume file.

**Headers:** 
- `Authorization: Bearer {token}`
- `Content-Type: multipart/form-data`

**Request Body (FormData):**
- `resume_file`: File upload (PDF, DOC, DOCX)

**Response (201):**
```json
{
  "message": "Resume uploaded successfully",
  "resume_id": 789,
  "filename": "john_doe_resume.pdf",
  "parsed_content": "Extracted text content...",
  "skills_extracted": ["JavaScript", "Python", "React"],
  "experience_years": 5
}
```

#### GET /resume
Get user's uploaded resumes.

**Headers:** `Authorization: Bearer {token}`

**Response:**
```json
{
  "resumes": [
    {
      "id": 789,
      "filename": "john_doe_resume.pdf",
      "uploaded_at": "2025-08-01T10:00:00Z",
      "skills_extracted": ["JavaScript", "Python", "React"],
      "experience_years": 5
    }
  ]
}
```

### Skills Management

#### POST /skills
Add technical skills.

**Headers:** `Authorization: Bearer {token}`

**Request Body:**
```json
{
  "skills": [
    {
      "skill_name": "JavaScript",
      "proficiency_level": "Advanced",
      "years_experience": 5
    },
    {
      "skill_name": "Python",
      "proficiency_level": "Intermediate",
      "years_experience": 3
    }
  ]
}
```

#### GET /skills
Get user's skills.

**Headers:** `Authorization: Bearer {token}`

**Response:**
```json
{
  "skills": [
    {
      "id": 1,
      "skill_name": "JavaScript",
      "proficiency_level": "Advanced",
      "years_experience": 5
    }
  ]
}
```

### Enhanced Application

#### POST /apply
Google-specific application.

**Headers:** `Authorization: Bearer {token}`

**Request Body:**
```json
{
  "job_id": 1,
  "cover_letter": "Cover letter...",
  "why_google": "Why I want to work at Google...",
  "relevant_experience": "Relevant experience description...",
  "coding_challenge_completed": true
}
```

---

## 5. Common Response Patterns

### Success Responses
- `200 OK`: Successful GET, PUT, DELETE
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE with no content

### Error Responses

#### 400 Bad Request
```json
{
  "error": "Validation failed",
  "details": {
    "email": "Invalid email format",
    "password": "Password must be at least 8 characters"
  }
}
```

#### 401 Unauthorized
```json
{
  "error": "Invalid credentials",
  "message": "Email or password is incorrect"
}
```

#### 403 Forbidden
```json
{
  "error": "Access denied",
  "message": "You don't have permission to access this resource"
}
```

#### 404 Not Found
```json
{
  "error": "Resource not found",
  "message": "Job with ID 999 does not exist"
}
```

#### 409 Conflict
```json
{
  "error": "Resource already exists",
  "message": "User has already applied to this job"
}
```

#### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

---

## 6. Authentication & Security

### JWT Token Format
All portals use JWT tokens with the following payload:
```json
{
  "user_id": 123,
  "email": "user@example.com",
  "portal": "meta",
  "iat": 1659283200,
  "exp": 1659369600
}
```

### Rate Limiting
- **Authentication endpoints**: 5 requests per minute per IP
- **Application endpoints**: 10 requests per minute per user
- **Job listing endpoints**: 100 requests per minute per IP

### CORS Configuration
All portals allow cross-origin requests from:
- `http://localhost:3000` (JAPS Main)
- `http://localhost:3001` (Meta)
- `http://localhost:3002` (Amazon)
- `http://localhost:3003` (Google)

---

## 7. Testing Endpoints

### Health Check (All Portals)

#### GET /health
Check service health.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-08-01T12:00:00Z",
  "version": "1.0.0",
  "database": "connected"
}
```

### Development Endpoints (Non-Production)

#### POST /dev/reset-db
Reset database to initial state (test data only).

**Response:**
```json
{
  "message": "Database reset successfully",
  "sample_users_created": 5,
  "sample_jobs_created": 10
}
```

#### GET /dev/test-data
Get test user credentials for automation.

**Response:**
```json
{
  "test_users": [
    {
      "email": "test.user1@example.com",
      "password": "TestPass123",
      "role": "applicant"
    }
  ]
}
```

This API specification provides comprehensive endpoints for all automation testing scenarios and realistic job application workflows.
