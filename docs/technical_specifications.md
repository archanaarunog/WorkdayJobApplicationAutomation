# Technical Implementation Specifications - JAPS

## Overview
This document provides detailed technical specifications for implementing each component of the Job Application Portal System (JAPS). Each section includes implementation requirements, acceptance criteria, and coding guidelines before development begins.

---

## 1. Meta Portal Implementation Spec

### 1.1 Backend Service (meta-service)

#### Technology Stack
- **Framework**: FastAPI 0.100+
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT tokens with python-jose
- **Validation**: Pydantic models
- **Testing**: pytest with test coverage >80%

#### File Structure
```
services/meta-service/
├── src/
│   ├── main.py              # FastAPI application entry
│   ├── config/
│   │   ├── __init__.py
│   │   ├── database.py      # Database configuration
│   │   └── settings.py      # Environment variables
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py          # User SQLAlchemy model
│   │   ├── job.py           # Job SQLAlchemy model
│   │   └── application.py   # Application SQLAlchemy model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py          # Pydantic schemas
│   │   ├── job.py           # Pydantic schemas
│   │   └── application.py   # Pydantic schemas
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── jobs.py          # Job-related endpoints
│   │   ├── applications.py  # Application endpoints
│   │   └── profile.py       # User profile endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py  # Business logic for auth
│   │   ├── job_service.py   # Business logic for jobs
│   │   └── user_service.py  # Business logic for users
│   └── utils/
│       ├── __init__.py
│       ├── security.py      # Password hashing, JWT
│       ├── validators.py    # Custom validators
│       └── exceptions.py    # Custom exceptions
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   ├── test_auth.py         # Authentication tests
│   ├── test_jobs.py         # Job endpoint tests
│   └── test_applications.py # Application tests
├── requirements.txt
├── Dockerfile
└── README.md
```

#### Implementation Requirements

**1. Database Connection (database.py)**
```python
# Required functionality:
- SQLite database connection with SQLAlchemy
- Database session management
- Connection pooling for concurrent requests
- Database initialization and table creation
```

**Acceptance Criteria:**
- [ ] Database connection established on startup
- [ ] Tables created automatically if not exist
- [ ] Session management with dependency injection
- [ ] Proper connection cleanup on shutdown

**2. User Model (models/user.py)**
```python
# Required fields and constraints:
- id: Primary key, auto-increment
- email: Unique, not null, email validation
- password_hash: Not null, minimum 60 chars (bcrypt)
- first_name: Not null, max 100 chars
- last_name: Not null, max 100 chars
- phone: Optional, regex validation
- created_at: Timestamp, default current
- updated_at: Timestamp, auto-update
- is_active: Boolean, default True
```

**Acceptance Criteria:**
- [ ] Model validates email format
- [ ] Password hashing implemented
- [ ] Proper table relationships defined
- [ ] Timestamps auto-managed

**3. Authentication Service (services/auth_service.py)**
```python
# Required methods:
- register_user(user_data) -> User
- authenticate_user(email, password) -> User | None
- create_access_token(user_id) -> str
- verify_token(token) -> User | None
- logout_user(token) -> bool
```

**Acceptance Criteria:**
- [ ] Password hashing with bcrypt (cost factor 12)
- [ ] JWT tokens expire in 24 hours
- [ ] Email uniqueness validation
- [ ] Secure password requirements (8+ chars, mixed case, numbers)
- [ ] Token blacklisting for logout

**4. API Endpoints (routes/auth.py)**
```python
# Required endpoints:
POST /api/register    # User registration
POST /api/login       # User authentication  
POST /api/logout      # Token invalidation
GET  /api/profile     # Get user profile
PUT  /api/profile     # Update user profile
```

**Acceptance Criteria:**
- [ ] All endpoints return consistent JSON responses
- [ ] Proper HTTP status codes (201, 200, 400, 401, 409)
- [ ] Request/response validation with Pydantic
- [ ] Error handling with descriptive messages
- [ ] Rate limiting implemented

### 1.2 Frontend Implementation (meta-ui)

#### Technology Stack
- **Core**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Simple, clean design (no frameworks)
- **HTTP**: Fetch API for backend communication
- **Testing**: Manual testing checklist

#### File Structure
```
frontend/meta-ui/
├── public/
│   ├── index.html           # Landing page
│   ├── login.html           # Login form
│   ├── register.html        # Registration form
│   ├── jobs.html            # Job listings
│   ├── apply.html           # Application form
│   └── profile.html         # User profile
├── assets/
│   ├── css/
│   │   ├── styles.css       # Main stylesheet
│   │   └── forms.css        # Form-specific styles
│   ├── js/
│   │   ├── main.js          # Core JavaScript
│   │   ├── auth.js          # Authentication logic
│   │   ├── jobs.js          # Job-related functions
│   │   └── api.js           # API communication
│   └── images/
│       └── meta-logo.png    # Company branding
├── Dockerfile
└── README.md
```

#### Implementation Requirements

**1. Authentication Pages**
```html
<!-- register.html requirements: -->
- Email input with validation
- Password input with strength indicator
- First name, last name inputs
- Optional phone number input
- Form validation before submission
- Error message display area
- Redirect to login after successful registration
```

**Acceptance Criteria:**
- [ ] Client-side email format validation
- [ ] Password strength requirements enforced
- [ ] Form submission handles errors gracefully
- [ ] Success/error messages displayed clearly
- [ ] Responsive design for mobile devices

**2. Job Listings (jobs.html)**
```html
<!-- Required features: -->
- Display job cards with title, location, salary
- Search functionality (title, location)
- Filter by job type, experience level
- Pagination (10 jobs per page)
- "Apply" button for authenticated users
- Login prompt for non-authenticated users
```

**Acceptance Criteria:**
- [ ] Jobs load from API on page load
- [ ] Search updates results in real-time
- [ ] Filters work independently and together
- [ ] Pagination navigation functional
- [ ] Apply button shows authentication status

**3. Application Form (apply.html)**
```html
<!-- Required fields: -->
- Job details display (read-only)
- Cover letter textarea (required, max 1000 chars)
- Additional information textarea (optional)
- Submit button with loading state
- Cancel/back navigation
```

**Acceptance Criteria:**
- [ ] Job details populate from URL parameter
- [ ] Character count for text areas
- [ ] Form validation before submission
- [ ] Loading states during API calls
- [ ] Success/error handling with user feedback

**4. JavaScript API Layer (assets/js/api.js)**
```javascript
// Required functions:
- registerUser(userData) -> Promise
- loginUser(credentials) -> Promise
- getJobs(filters) -> Promise
- getJobById(jobId) -> Promise
- submitApplication(applicationData) -> Promise
- getUserProfile() -> Promise
- updateUserProfile(userData) -> Promise
```

**Acceptance Criteria:**
- [ ] All functions return standardized Promise responses
- [ ] JWT token management (localStorage)
- [ ] Automatic token inclusion in requests
- [ ] Error handling with user-friendly messages
- [ ] Request/response logging for debugging

---

## 2. Amazon Portal Implementation Spec

### 2.1 Enhanced Backend Features

#### Additional Models Required

**Work Experience Model (models/experience.py)**
```python
# Required fields:
- id: Primary key
- user_id: Foreign key to users
- company_name: Not null, max 100 chars
- job_title: Not null, max 100 chars
- start_date: Date, not null
- end_date: Date, nullable (for current jobs)
- description: Text, optional
- is_current: Boolean, default False
```

**Education Model (models/education.py)**
```python
# Required fields:
- id: Primary key
- user_id: Foreign key to users
- school_name: Not null, max 200 chars
- degree: Not null, max 100 chars
- field_of_study: Max 100 chars
- graduation_year: Integer, validation (1950-2030)
- gpa: Decimal(3,2), optional
```

#### Extended API Endpoints
```python
# Additional endpoints for Amazon:
POST /api/experience      # Add work experience
GET  /api/experience      # Get user's experience
PUT  /api/experience/{id} # Update experience
DELETE /api/experience/{id} # Delete experience

POST /api/education       # Add education
GET  /api/education       # Get user's education
PUT  /api/education/{id}  # Update education
DELETE /api/education/{id} # Delete education
```

**Acceptance Criteria:**
- [ ] CRUD operations for experience and education
- [ ] Proper validation for dates and GPA
- [ ] Authorization checks (users can only modify own data)
- [ ] Cascading delete when user is deleted

### 2.2 React Frontend (amazon-ui)

#### Technology Stack
- **Framework**: React 18+ with JavaScript (not TypeScript)
- **State Management**: React hooks (useState, useEffect, useContext)
- **Routing**: React Router DOM
- **HTTP**: Axios for API communication
- **UI Library**: Material-UI (MUI)
- **Build Tool**: Create React App

#### Component Structure
```
frontend/amazon-ui/
├── public/
│   ├── index.html
│   └── favicon.ico
├── src/
│   ├── components/
│   │   ├── common/
│   │   │   ├── Header.js
│   │   │   ├── Footer.js
│   │   │   ├── Loading.js
│   │   │   └── ErrorBoundary.js
│   │   ├── auth/
│   │   │   ├── LoginForm.js
│   │   │   ├── RegisterForm.js
│   │   │   └── ProtectedRoute.js
│   │   ├── jobs/
│   │   │   ├── JobList.js
│   │   │   ├── JobCard.js
│   │   │   ├── JobDetails.js
│   │   │   └── JobFilters.js
│   │   ├── profile/
│   │   │   ├── ProfileForm.js
│   │   │   ├── ExperienceForm.js
│   │   │   ├── EducationForm.js
│   │   │   └── ProfileTabs.js
│   │   └── application/
│   │       ├── ApplicationForm.js
│   │       ├── ApplicationList.js
│   │       └── ApplicationStatus.js
│   ├── pages/
│   │   ├── HomePage.js
│   │   ├── LoginPage.js
│   │   ├── RegisterPage.js
│   │   ├── JobsPage.js
│   │   ├── ApplicationPage.js
│   │   └── ProfilePage.js
│   ├── services/
│   │   ├── api.js
│   │   ├── auth.js
│   │   └── jobs.js
│   ├── context/
│   │   └── AuthContext.js
│   ├── hooks/
│   │   ├── useAuth.js
│   │   └── useApi.js
│   ├── utils/
│   │   ├── constants.js
│   │   ├── helpers.js
│   │   └── validators.js
│   ├── App.js
│   └── index.js
├── package.json
├── Dockerfile
└── README.md
```

#### Implementation Requirements

**1. Authentication Context (context/AuthContext.js)**
```javascript
// Required functionality:
- User state management
- Login/logout functions
- Token management
- Authentication status
- User profile data
```

**Acceptance Criteria:**
- [ ] Context provides authentication state to all components
- [ ] Automatic token refresh logic
- [ ] Persistent login across browser sessions
- [ ] Logout clears all user data
- [ ] Loading states during authentication

**2. Job List Component (components/jobs/JobList.js)**
```javascript
// Required features:
- Display jobs in card format using MUI Cards
- Pagination with MUI Pagination component
- Search and filter functionality
- Loading and error states
- Responsive grid layout
```

**Acceptance Criteria:**
- [ ] Jobs load on component mount
- [ ] Search updates results with debounced input
- [ ] Filters persist across page navigation
- [ ] Loading skeleton during data fetch
- [ ] Error handling with retry option

**3. Enhanced Application Form (components/application/ApplicationForm.js)**
```javascript
// Required fields (Amazon-specific):
- Cover letter (required, rich text editor)
- Why Amazon essay (required, 500 word limit)
- Availability date picker
- Willing to relocate checkbox
- Salary expectation input
- Work authorization status
```

**Acceptance Criteria:**
- [ ] Form validation with MUI form helpers
- [ ] Character/word count indicators
- [ ] Date picker with future date validation
- [ ] Salary format validation
- [ ] Draft save functionality
- [ ] Submit confirmation dialog

---

## 3. Google Portal Implementation Spec

### 3.1 Advanced Backend Features

#### Resume Processing Service
```python
# Required functionality (services/resume_service.py):
- upload_resume(user_id, file) -> Resume
- parse_resume_content(file_path) -> Dict
- extract_skills(text_content) -> List[str]
- calculate_experience_years(text_content) -> int
- validate_file_type(file) -> bool
- compress_file(file_path) -> str
```

**Acceptance Criteria:**
- [ ] Support PDF, DOC, DOCX file formats
- [ ] File size limit validation (5MB max)
- [ ] Text extraction from uploaded files
- [ ] Basic skill recognition (keyword matching)
- [ ] Experience calculation from dates in resume
- [ ] File storage with unique naming

#### Skills Management Service
```python
# Required functionality (services/skills_service.py):
- add_user_skill(user_id, skill_data) -> Skill
- get_user_skills(user_id) -> List[Skill]
- update_skill_proficiency(skill_id, level) -> Skill
- suggest_skills(resume_content) -> List[str]
- validate_proficiency_level(level) -> bool
```

**Acceptance Criteria:**
- [ ] Skill proficiency levels: Beginner, Intermediate, Advanced, Expert
- [ ] Duplicate skill prevention for same user
- [ ] Skills extracted from resume auto-populate form
- [ ] Years of experience validation (0-50 range)

### 3.2 React Frontend with Advanced Features

#### Enhanced Components

**Resume Upload Component (components/resume/ResumeUpload.js)**
```javascript
// Required features:
- Drag and drop file upload
- File format validation
- Upload progress indicator
- Resume preview after upload
- Skills extraction display
- Multiple resume management
```

**Acceptance Criteria:**
- [ ] Visual drag-and-drop zone with MUI styling
- [ ] File format validation before upload
- [ ] Progress bar during upload
- [ ] Extracted text preview
- [ ] Auto-populated skills from resume
- [ ] Delete/replace resume functionality

**Skills Management Component (components/profile/SkillsManager.js)**
```javascript
// Required features:
- Add skills with autocomplete
- Proficiency level selection
- Years of experience input
- Skills from resume integration
- Skill category grouping
- Export skills summary
```

**Acceptance Criteria:**
- [ ] Autocomplete with common tech skills
- [ ] Visual proficiency indicators (progress bars)
- [ ] Skills grouped by category (Frontend, Backend, etc.)
- [ ] Integration with resume-extracted skills
- [ ] Bulk edit functionality

---

## 4. JAPS Main Portal Implementation Spec

### 4.1 Job Aggregation Service

#### Technology Stack
- **Backend**: FastAPI with async/await
- **Frontend**: React with Material-UI
- **Job Sync**: APScheduler for periodic updates
- **Caching**: Redis (optional, or in-memory for simplicity)

#### Core Aggregation Logic
```python
# Required functionality (services/aggregation_service.py):
- sync_jobs_from_all_portals() -> Dict[str, int]
- fetch_jobs_from_portal(portal_url) -> List[Job]
- merge_and_deduplicate_jobs(jobs_list) -> List[Job]
- update_job_sync_status(company_id, status) -> None
- get_aggregated_jobs(filters) -> List[Job]
```

**Acceptance Criteria:**
- [ ] Periodic job sync every 30 minutes
- [ ] Error handling for failed portal connections
- [ ] Job deduplication by title and company
- [ ] Sync status tracking and logging
- [ ] Manual sync trigger for admin users

#### Search and Filter Engine
```python
# Required functionality (services/search_service.py):
- search_jobs(query, filters) -> List[Job]
- filter_by_location(jobs, location) -> List[Job]
- filter_by_salary_range(jobs, min_sal, max_sal) -> List[Job]
- filter_by_company(jobs, company_names) -> List[Job]
- sort_jobs(jobs, sort_by, order) -> List[Job]
```

**Acceptance Criteria:**
- [ ] Full-text search across job titles and descriptions
- [ ] Multiple filter combination support
- [ ] Salary range filtering with proper number handling
- [ ] Sort by relevance, date, salary
- [ ] Pagination with configurable page sizes

### 4.2 React Dashboard Frontend

#### Main Dashboard Component
```javascript
// Required features (components/dashboard/JobDashboard.js):
- Company portal status indicators
- Total job count from each portal
- Search bar with advanced filters
- Job results grid with company logos
- Apply button redirects to company portals
- Recent sync status display
```

**Acceptance Criteria:**
- [ ] Real-time portal health status
- [ ] Visual job count breakdown by company
- [ ] Advanced search with multiple criteria
- [ ] Job cards with company branding
- [ ] Smooth redirect to company application pages
- [ ] Sync status with last update timestamps

---

## 5. Docker & Deployment Specifications

### 5.1 Individual Service Dockerfiles

#### Backend Service Dockerfile Template
```dockerfile
# Required for all FastAPI services:
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### React Frontend Dockerfile Template
```dockerfile
# Required for React services:
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY public/ ./public/
COPY src/ ./src/
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### 5.2 Docker Compose Configuration

#### Main docker-compose.yml
```yaml
# Required services and configuration:
services:
  japs-main:
    build: ./services/japs-main-service
    ports: ["3000:8000"]
    environment:
      - DATABASE_URL=sqlite:///databases/japs_main.db
      - SECRET_KEY=${JWT_SECRET_KEY}
    volumes: ["./databases:/app/databases"]
    
  meta-service:
    build: ./services/meta-service
    ports: ["3001:8000"]
    environment:
      - DATABASE_URL=sqlite:///databases/meta.db
      - SECRET_KEY=${JWT_SECRET_KEY}
    volumes: ["./databases:/app/databases"]
    
  # Similar configuration for amazon-service and google-service
  
volumes:
  databases:
networks:
  japs-network:
    driver: bridge
```

**Acceptance Criteria:**
- [ ] All services start with single command
- [ ] Database persistence across container restarts
- [ ] Environment variable configuration
- [ ] Service-to-service communication
- [ ] Health check endpoints

---

## 6. Testing Implementation Requirements

### 6.1 Backend Testing Strategy

#### Unit Tests (pytest)
```python
# Required test coverage:
- Authentication service: 90%+ coverage
- Job service: 85%+ coverage
- Application service: 85%+ coverage
- Database models: 90%+ coverage
- API endpoints: 80%+ coverage
```

#### Integration Tests
```python
# Required test scenarios:
- Full registration → login → job application flow
- Cross-portal job aggregation accuracy
- File upload and processing (Google portal)
- Database transaction integrity
- API error handling and edge cases
```

**Acceptance Criteria:**
- [ ] All tests run with `pytest` command
- [ ] Test database isolation (separate test DB)
- [ ] Fixtures for common test data
- [ ] API endpoint testing with test client
- [ ] Mock external dependencies

### 6.2 Frontend Testing Strategy

#### Component Testing (React Testing Library)
```javascript
// Required test coverage:
- Authentication components: 80%+ coverage
- Job listing components: 75%+ coverage
- Form components: 85%+ coverage
- API service functions: 90%+ coverage
```

#### End-to-End Testing (Automation Ready)
```javascript
// Required test scenarios:
- Complete user registration and login flow
- Job search and filter functionality
- Job application submission process
- Cross-portal navigation and redirects
- Form validation and error handling
```

**Acceptance Criteria:**
- [ ] All components render without errors
- [ ] User interactions trigger expected behaviors
- [ ] API calls handled correctly
- [ ] Error states displayed appropriately
- [ ] Responsive design tested on multiple screen sizes

---

## 7. Quality Assurance Standards

### 7.1 Code Quality Requirements

#### Python Code Standards
- **Linting**: flake8 with max line length 88
- **Formatting**: black formatter
- **Type Hints**: mypy for static type checking
- **Documentation**: docstrings for all public functions
- **Security**: bandit for security issue detection

#### JavaScript Code Standards
- **Linting**: ESLint with React plugin
- **Formatting**: Prettier
- **Documentation**: JSDoc for complex functions
- **Performance**: React DevTools profiling
- **Accessibility**: WCAG 2.1 AA compliance

### 7.2 Performance Requirements

#### Backend Performance
- **Response Time**: < 200ms for simple queries
- **Database**: Query optimization with indexing
- **Concurrency**: Handle 100 concurrent users
- **Memory**: < 512MB per service
- **Startup Time**: < 10 seconds

#### Frontend Performance
- **Page Load**: < 3 seconds initial load
- **Bundle Size**: < 2MB total JavaScript
- **Image Optimization**: WebP format, lazy loading
- **Caching**: Service worker for offline capability
- **Lighthouse Score**: > 90 for Performance

### 7.3 Security Requirements

#### Authentication Security
- **Password Hashing**: bcrypt with cost factor 12
- **JWT Security**: Short expiration, secure signing
- **Session Management**: Secure token storage
- **CORS**: Properly configured origins
- **HTTPS**: SSL/TLS in production

#### Data Protection
- **Input Validation**: All user inputs sanitized
- **SQL Injection**: Parameterized queries only
- **File Upload**: Type and size validation
- **Error Handling**: No sensitive data in error messages
- **Logging**: Security events logged

---

## 8. Documentation Requirements

### 8.1 Developer Documentation

#### API Documentation
- **OpenAPI/Swagger**: Auto-generated from FastAPI
- **Postman Collection**: Complete endpoint testing
- **Examples**: Request/response samples for all endpoints
- **Error Codes**: Complete error handling documentation

#### Setup Documentation
- **Installation Guide**: Step-by-step local setup
- **Environment Variables**: Complete configuration list
- **Database Setup**: Schema creation and seeding
- **Testing Guide**: How to run all test suites

### 8.2 User Documentation

#### Automation Testing Guide
- **Test Scenarios**: Complete user journey documentation
- **Test Data**: Sample data for automation scripts
- **Locators**: CSS/XPath selectors for key elements
- **API Testing**: cURL examples for all endpoints

This comprehensive technical specification ensures that every component has clear implementation requirements, acceptance criteria, and quality standards before any coding begins. This follows enterprise development practices and supports the automation testing goals of the project.
