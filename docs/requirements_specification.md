# Requirements Specification - Job Application Portal System (JAPS)

**Document Version:** 1.0  
**Date:** July 31, 2025  
**Project Manager:** Archana Arun  
**Status:** Draft

---

## 1. Introduction

### 1.1 Purpose
This document specifies the functional and non-functional requirements for the Job Application Portal System (JAPS), a multi-portal mock system designed to demonstrate automated job application capabilities across different company platforms. The system enables automated form filling, profile management, and application submission using extracted resume data and user preferences.

### 1.2 Scope
JAPS consists of:
- **Main Portal:** Central job aggregator (like Indeed)
- **Company Portals:** 3 separate company application systems
  - Meta Portal
  - Amazon Portal  
  - Google Portal

### 1.3 Definitions
- **Job Seeker:** End user applying for jobs through automated system
- **Portal:** Individual company website/application platform
- **Application Flow:** Complete automated process from job discovery to application submission
- **Automation Framework:** System that automatically fills forms and submits applications
- **Profile Engine:** Component that manages and maps user data to different portal requirements

---

## 2. System Overview

### 2.1 System Architecture
```
User Journey:
JAPS Main Portal → Browse Jobs → Click Apply → 
Company Portal → Register/Login → Fill Application → Submit
```

### 2.2 System Components
| Component | URL | Technology | Purpose |
|-----------|-----|------------|---------|
| JAPS Main | localhost:3000 | React + FastAPI | Job aggregation & browsing |
| Meta | localhost:3001 | HTML/CSS + FastAPI | Simple application portal |
| Amazon | localhost:3002 | React + FastAPI | Medium complexity portal |
| Google | localhost:3003 | React + FastAPI | Advanced portal with uploads |

---

## 3. Functional Requirements

### 3.1 JAPS Main Portal Requirements

#### 3.1.1 Job Browsing (FR-001)
- **Description:** Users can browse jobs from multiple companies
- **Acceptance Criteria:**
  - Display 10-15 sample jobs from 3 companies
  - Show job title, company, location, salary range
  - Filter by: location, job type, company
  - Search by keywords
- **Priority:** High

#### 3.1.2 Job Details View (FR-002)
- **Description:** Users can view detailed job information
- **Acceptance Criteria:**
  - Job description, requirements, benefits
  - Company information
  - "Apply Now" button redirects to company portal
- **Priority:** High

#### 3.1.3 Company Directory (FR-003)
- **Description:** List of participating companies
- **Acceptance Criteria:**
  - Company name, logo, description
  - Number of open positions
  - Link to company portal
- **Priority:** Medium

### 3.2 Company Portal Requirements

#### 3.2.1 User Registration (FR-004)
- **Description:** Job seekers create accounts on company portals
- **Acceptance Criteria:**
  - Email/password registration
  - Google OAuth (Amazon and Google only)
  - Email verification (simulated)
  - Form validation
- **Priority:** High

#### 3.2.2 User Authentication (FR-005)
- **Description:** Secure login to company portals
- **Acceptance Criteria:**
  - Login with email/password
  - Session management
  - "Remember me" option
  - Password reset functionality (simulated)
- **Priority:** High

#### 3.2.3 Profile Management (FR-006)
- **Description:** Users maintain their profile information
- **Required Fields:**
  - Full name, email, phone number
  - Current location, work authorization
  - LinkedIn URL
  - Education details (degree, institution, year)
  - Work experience (company, role, duration)
  - Skills (comma-separated)
  - Privacy agreement acceptance
- **Priority:** High

#### 3.2.4 Resume Upload & Parsing (FR-007)
- **Description:** Users upload resume and system extracts information
- **Acceptance Criteria:**
  - Support PDF and DOC formats
  - Extract text from resume
  - Auto-populate profile fields where possible
  - Manual override capability
- **Priority:** Medium (Google only)

#### 3.2.5 Job Application Submission (FR-008)
- **Description:** Users complete and submit job applications
- **Acceptance Criteria:**
  - Pre-populated from profile data
  - Company-specific questions
  - Cover letter text area
  - Application status tracking
  - Confirmation email (simulated)
- **Priority:** High

### 3.3 Portal-Specific Features

#### 3.3.1 Meta Portal (Simple)
- Basic email/password registration
- Minimal form fields
- No file uploads
- Simple validation

#### 3.3.2 Amazon Portal (Medium)
- Email/password + Google OAuth
- Moderate form complexity
- Basic profile management
- Input validation

#### 3.3.3 Google Portal (Advanced)
- Full authentication options
- Resume upload capability
- Complex multi-step forms
- Advanced validation

---

## 4. Non-Functional Requirements

### 4.1 Performance Requirements (NFR-001)
- **Page Load Time:** ≤ 3-5 seconds
- **Concurrent Users:** Support 50 simultaneous users
- **Response Time:** API calls ≤ 2 seconds
- **Database Queries:** ≤ 1 second

### 4.2 Usability Requirements (NFR-002)
- **Browser Support:** Chrome, Firefox (latest versions)
- **Device Support:** Desktop only (responsive design)
- **Accessibility:** Basic WCAG 2.1 guidelines
- **Language:** English only

### 4.3 Security Requirements (NFR-003)
- **Password Policy:** Minimum 8 characters
- **Data Encryption:** Passwords hashed
- **Session Management:** 30-minute timeout
- **Input Validation:** All form inputs validated

### 4.4 Reliability Requirements (NFR-004)
- **Availability:** 99% uptime (development environment)
- **Error Handling:** Graceful error messages
- **Data Backup:** Local SQLite backups
- **Recovery:** Manual restart capability

---

## 5. Technical Requirements

### 5.1 Technology Stack (Learning-Optimized)
```
Frontend:
- React 18+ with JavaScript (focus on JS mastery first)
- Material-UI components
- HTML5/CSS3 (for Meta portal)

Future Enhancement:
- TypeScript migration (Phase 2 learning goal)

Backend:
- Python FastAPI (all portals for consistency)
- SQLite database (separate per portal)
- Pydantic for validation

Development Tools:
- Docker for containerization
- Git for version control
- pytest for testing

Authentication:
- JWT tokens (real implementation)
- Simulated OAuth (fake buttons for learning)
- Basic session management

Resume Parsing:
- PyPDF2 for PDF text extraction
- Basic regex for data extraction
- Manual field mapping interface
```

### 5.2 Database Requirements
- **Users Table:** Store user profiles
- **Jobs Table:** Job listings and details
- **Companies Table:** Company information
- **Applications Table:** Application submissions
- **Sessions Table:** User session management

### 5.3 API Requirements
- **RESTful APIs:** JSON request/response
- **Authentication:** JWT tokens
- **Documentation:** OpenAPI/Swagger
- **Validation:** Request/response validation

---

## 6. User Interface Requirements

### 6.1 Design Guidelines
- **Style:** Professional corporate appearance
- **Color Scheme:** Blue/gray corporate palette
- **Typography:** Clean, readable fonts
- **Layout:** Responsive grid system

### 6.2 Navigation Requirements
- **Main Navigation:** Top horizontal menu
- **Breadcrumbs:** Show user location
- **Footer:** Links and company info
- **Search:** Prominent search functionality

### 6.3 Form Design
- **Validation:** Real-time field validation
- **Error Messages:** Clear, helpful messaging
- **Progress Indicators:** Multi-step form progress
- **Accessibility:** Proper labels and ARIA attributes

---

## 7. Integration Requirements

### 7.1 Inter-Portal Communication
- **Job Data Sync:** JAPS pulls from company databases
- **Application Tracking:** Status updates between systems
- **User Redirection:** Seamless portal transitions

### 7.2 External Integrations
- **Google OAuth:** Authentication service
- **Resume Parsing:** Python text extraction libraries
- **Email Simulation:** Console logging for emails

---

## 8. Data Requirements

### 8.1 Sample Data
- **Companies:** 3 FANG companies with profiles
- **Jobs:** 10-15 diverse job postings
- **Users:** 5 test user accounts
- **Applications:** Sample application data

### 8.2 Data Validation
- **Email Format:** Valid email patterns
- **Phone Numbers:** US format validation
- **Required Fields:** Mandatory field enforcement
- **File Types:** PDF/DOC validation for uploads

---

## 9. Testing Requirements

### 9.1 Functional Testing
- **User Registration:** All registration flows
- **Job Application:** End-to-end application process
- **Authentication:** Login/logout functionality
- **Data Validation:** Form validation testing

### 9.2 Cross-Portal Testing
- **Navigation Flow:** JAPS → Company portal → Application
- **Data Consistency:** Profile data across portals
- **Session Management:** Login state maintenance

---

## 10. Deployment Requirements

### 10.1 Local Development
- **Docker Compose:** Single-command startup
- **Port Configuration:** Unique ports for each portal
- **Database Setup:** Automated schema creation
- **Sample Data:** Pre-populated test data

### 10.2 Repository Setup
- **Documentation:** Clear setup instructions
- **Scripts:** Automated startup scripts
- **Environment:** Configuration management
- **Demo:** Video or live demonstration capability

---

## 11. Success Criteria

### 11.1 Functional Success
- [ ] All 4 portals operational
- [ ] Complete user journey working
- [ ] Data persistence functional
- [ ] Cross-portal navigation working

### 11.2 Automation Success
- [ ] Automated profile data extraction from resume
- [ ] Cross-platform form filling capabilities demonstrated
- [ ] Multiple portal automation workflows operational
- [ ] Portfolio showcasing automation engineering skills

---

## 12. Assumptions and Dependencies

### 12.1 Assumptions
- Development on macOS environment
- Local development only (no cloud deployment)
- Single developer working alone
- 7-hour development timeframe

### 12.2 Dependencies
- Docker and Docker Compose installed
- Node.js and Python environments
- Git repository access
- Modern web browser for testing

---

## 13. Risks and Mitigation

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Time constraints | High | Medium | Prioritize core features, defer nice-to-have |
| Technical complexity | Medium | Medium | Start simple, iterate and improve |
| Integration issues | Medium | Low | Use standard APIs, test frequently |
| Learning curve | Low | High | Focus on documentation and examples |

---

**Document Approval:**
- **Business Analyst:** Archana Arun ✓
- **Technical Lead:** Archana Arun ✓  
- **Project Manager:** Archana Arun ✓

**Next Steps:** Proceed to System Design phase
