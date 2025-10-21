# Daily Task Management - JAPS
#
# ---
#
# v1.0.0 Features (Completed)
# - User registration and login with JWT authentication
# - Job listing and job details view
# - Apply to jobs with cover letter (modal form)
# - Secure password hashing (bcrypt)
# - SQLite database with SQLAlchemy models (User, Job, Application)
# - API documentation (Swagger UI)
# - CORS enabled for frontend-backend integration
# - Responsive UI with Bootstrap 5
# - Modular project structure (backend/frontend separation)
# - Basic error handling and validation
# - Project documentation and setup instructions
#
# ---
#
# v1.1.0 Features (Planned)
# - User application history/profile page (view jobs applied to)
# - Admin dashboard (manage jobs, view all applications, user management)
# - Enhanced error handling and user feedback (frontend/backend)
# - Input validation improvements (frontend/backend)
# - Password reset/change functionality
# - Pagination and filtering for job listings
# - UI/UX improvements:
#   - Improved navigation bar and page layout
#   - Loading indicators and better modals
#   - Consistent color scheme and branding
#   - Mobile responsiveness and accessibility
# - API security hardening (rate limiting, improved JWT handling)
# - Documentation updates (usage examples, API docs, contribution guide)
# - Additional tests and test data


## Day 1: July 31, 2025 (4 Hours Available)

### Session Overview
**Time Available:** 4 hours  
**Goal:** Complete Planning & Requirements phases  
**Current Status:** Hour 1 completed (Project Charter ✓)

---

## Hour 1: Project Setup & Planning [COMPLETED ✓]
**Time:** 1 hour | **Status:** ✅ DONE
- [x] Project charter creation
- [x] Technology stack finalization  
- [x] Git repository setup
- [x] Development environment planning

---

## Hour 2: Requirements Documentation [COMPLETED ✓]
**Time:** 1 hour | **Status:** ✅ DONE
### Objectives:
- [x] **Functional Requirements (20 min)**
  - Core user flows (register, login, apply)
  - Job posting functionality
  - Application management features

- [x] **Technical Requirements (20 min)**
  - Performance criteria
  - Security requirements
  - Browser compatibility
  - API specifications

- [x] **Mock Site Requirements (20 min)**
  - UI/UX guidelines
  - Data models
  - Integration points
  - Validation rules

- [x] **Technology Stack Finalization**
  - Simplified stack for learning: JavaScript instead of TypeScript
  - Consistent backend: FastAPI across all portals
  - Database strategy: Separate SQLite per portal

### Technology Stack Summary:
**Frontend:**
- React 18+ with JavaScript (learning-friendly approach)
- Material-UI for components
- HTML5/CSS3 for Meta portal

**Backend:**
- Python FastAPI (standardized across all 4 portals)
- SQLite databases (separate per portal)
- JWT authentication

**Development:**
- Docker for containerization
- Git version control
- pytest for testing

**Future Learning Path:**
- TypeScript migration in Phase 2
- Advanced authentication systems
- Cloud deployment strategies

### Deliverables:
- [x] `requirements_specification.md`
- [ ] `user_stories.md`
- [x] Update tracking document
- [x] Technology stack documentation

---

## Hour 3: System Design [COMPLETED ✓]
**Time:** 1 hour | **Status:** ✅ DONE
### Objectives:
- [x] **System Architecture (20 min)**
  - Component diagram
  - Technology stack mapping
  - Data flow design

- [x] **Database Schema (20 min)**
  - Entity relationship diagram
  - Table structures
  - Data relationships

- [x] **API Endpoint Planning (20 min)**
  - REST API design
  - Endpoint documentation
  - Request/response formats

### Deliverables:
- [x] `system_architecture.md`
- [x] `database_schema.md`
- [x] `api_specifications.md`
- [x] `technical_specifications.md`
- [x] `user_stories.md`

---

## Hour 4: Meta Portal Implementation [COMPLETED ✓]
**Time:** 2.5 hours | **Status:** ✅ DONE
### Objectives:
- [x] **Project Structure Setup (15 min)**
  - Create folder structure for Meta Portal
  - Initialize backend and frontend directories
  - Set up basic configuration files

- [x] **Meta Backend Foundation (90 min)**
  - FastAPI application setup with SQLAlchemy
  - Database models (User, Job, Application) with relationships
  - Pydantic schemas for API validation
  - Authentication endpoints (register, login) with JWT
  - Password hashing with bcrypt
  - Database connection and table creation
  - CORS middleware for frontend integration

- [x] **Virtual Environment & Dependencies (30 min)**
  - Python virtual environment configuration
  - Package installation: FastAPI, uvicorn, SQLAlchemy, passlib, python-jose, bcrypt, pydantic
  - Fixed import structure with proper relative imports
  - Database path configuration

### ✅ **COMPLETED BACKEND IMPLEMENTATION:**

#### 1. **Database Models Created:**
- `User` model: id, email, password_hash, first_name, last_name, phone, timestamps
- `Job` model: id, title, company, location, description, requirements, salary, timestamps
- `Application` model: id, user_id, job_id, cover_letter, status, timestamps
- All with proper SQLAlchemy relationships

#### 2. **Authentication System:**
- User registration endpoint: `POST /api/register`
- Login endpoint: `POST /api/login` 
- JWT token generation and validation
- Password hashing with bcrypt
- Phone number validation

#### 3. **API Endpoints Active:**
- Health check: `GET /` ✅
- Interactive API docs: `GET /docs` ✅
- User registration: `POST /api/register` ✅
- User login: `POST /api/login` ✅

#### 4. **Server Running Successfully:**
- **URL:** http://127.0.0.1:8000
- **API Docs:** http://127.0.0.1:8000/docs
- **Database:** SQLite at `/databases/meta.db`

### 🛠️ **COMMANDS EXECUTED:**

#### Virtual Environment Setup:
```bash
# Auto-configured virtual environment at:
# /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/.venv/

# Packages installed:
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
passlib==1.7.4
python-jose==3.3.0
bcrypt==4.3.0
pydantic==2.5.0
email-validator==2.1.0
```

#### Server Start Commands:
```bash
# Navigate to correct directory:
cd /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service

# Start server (current working command):
PYTHONPATH=/Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/.venv/bin/python -m uvicorn src.main:app --reload
```

### 🚀 **SIMPLIFIED COMMANDS FOR FUTURE USE:**

#### Create Aliases for Easy Development:
```bash
# Add to your ~/.zshrc or ~/.bashrc:
alias japs-venv="source /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/.venv/bin/activate"
alias japs-meta="cd /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service"
alias japs-server="PYTHONPATH=. ../../../.venv/bin/python -m uvicorn src.main:app --reload"

# Usage:
japs-meta && japs-server
```

#### Alternative: Using Relative Paths (when in meta-service directory):
```bash
# After: cd /Users/achu/.../services/meta-service
PYTHONPATH=. ../../../.venv/bin/python -m uvicorn src.main:app --reload
```

#### Virtual Environment Activation:
```bash
# From project root:
source .venv/bin/activate

# Then from meta-service directory:
python -m uvicorn src.main:app --reload
```

### 🔧 **KEY TECHNICAL FIXES:**

1. **Import Structure Fixed:**
   - Added `__init__.py` files to all packages
   - Standardized relative imports (`.config.database`, `.models`, etc.)
   - Fixed path resolution for database creation

2. **Database Path Correction:**
   - Fixed path calculation to use project root `/databases/` folder
   - Corrected from 4 to 5 levels up in directory structure

3. **Python Package Structure:**
   - Proper module structure with relative imports
   - PYTHONPATH configuration for module discovery
   - Consistent import patterns across all files

### ⚠️ **Known Issues Fixed:**
- ✅ "ModuleNotFoundError: No module named 'src'" - Fixed with PYTHONPATH
- ✅ "sqlite3.OperationalError: unable to open database file" - Fixed database path
- ✅ "ImportError: attempted relative import" - Fixed import structure
- ✅ "Address already in use" - Added proper process cleanup

### 📋 **Testing Completed:**
- ✅ Server startup without errors
- ✅ Health endpoint responding: `{"message":"Meta Portal API is running!"}`
- ✅ API documentation accessible at `/docs`
- ✅ Database tables created successfully
- ✅ CORS enabled for frontend integration

### Step-by-Step Meta Portal Breakdown:

#### Step 1: Folder Structure (5 min)
```
services/meta-service/
├── src/
│   ├── main.py
│   ├── config/
│   ├── models/
│   ├── routes/
│   ├── services/
│   └── utils/
├── requirements.txt
└── Dockerfile

frontend/meta-ui/
├── public/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── jobs.html
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── Dockerfile
```

#### Step 2: Backend Setup (20 min)
1. **Database Setup** (5 min)
   - Create SQLite database connection
   - User, Job, Application models
   
2. **Authentication Service** (10 min)
   - User registration endpoint
   - Login with JWT token generation
   - Password hashing with bcrypt

3. **Basic Job Service** (5 min)
   - Job listing endpoint
   - Job details endpoint
   - Sample job data seeding

#### Step 3: Frontend Setup (15 min)
1. **Registration Page** (5 min)
   - HTML form with required fields
   - Client-side validation
   - API integration

2. **Login Page** (5 min)
   - Login form
   - JWT token handling
   - Redirect logic

3. **Jobs Page** (5 min)
   - Job listing display
   - Basic styling
   - Apply button integration

### Deliverables:
- [x] Working Meta Portal backend (registration, login, health check)
- [x] Database models with proper relationships
- [x] JWT authentication system implemented
- [x] API documentation auto-generated
- [x] Virtual environment configured with all dependencies
- [x] Server running successfully on http://127.0.0.1:8000
- [ ] Frontend implementation (Next: HTML pages and JavaScript)
- [ ] Sample job data seeding
- [ ] Manual testing of complete user flow

---

## Daily Success Criteria
By end of Day 1, you should have:
- [x] Complete project documentation foundation
- [x] Clear requirements specification
- [x] System design blueprint
- [x] Complete Azure DevOps-style documentation suite
- [x] Working Meta Portal backend (registration, login, database)
- [x] FastAPI server running with JWT authentication
- [x] All documentation committed to Git
- [ ] Frontend HTML pages (Next session)

---

## Time Tracking
```
Hour 1: 1.5 hours (Setup + Charter) ✅
Hour 2: 1.0 hours (Requirements + Tech Stack) ✅  
Hour 3: 1.0 hours (Complete Documentation Suite) ✅
Hour 4: 2.5 hours (Meta Portal Backend Implementation) ✅
Total: 6.0/4 hours (Extended for comprehensive backend)
```

**Extended Session Accomplishments:**
- Spent extra time on proper backend architecture
- Resolved complex import structure issues
- Implemented complete authentication system
- Created production-ready database models
- Established solid foundation for remaining portals

---

## 🚀 **STREAMLINED DEVELOPMENT WORKFLOW**

### Quick Start Commands (Future Sessions):

#### Option 1: Using Aliases (Recommended)
```bash
# Add to ~/.zshrc:
alias japs-venv="source /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/.venv/bin/activate"
alias japs-meta="cd /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service"
alias japs-start="PYTHONPATH=. ../../../.venv/bin/python -m uvicorn src.main:app --reload"

# Usage (from anywhere):
japs-meta && japs-start
```

#### Option 2: Virtual Environment Activation
```bash
# From project root:
cd /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation
source .venv/bin/activate

# Navigate and start:
cd services/meta-service
python -m uvicorn src.main:app --reload
```

#### Option 3: One-liner (from meta-service directory)
```bash
cd /Users/achu/Documents/Workspace/WorkdayJobApplicationAutomation/services/meta-service
PYTHONPATH=. ../../../.venv/bin/python -m uvicorn src.main:app --reload
```

### Project Status Summary:
- ✅ **Backend:** Complete with authentication, database, API docs
- ✅ **Environment:** Virtual environment with all dependencies
- ✅ **Server:** Running at http://127.0.0.1:8000
- ⏳ **Frontend:** Ready for HTML/CSS/JavaScript implementation
- ⏳ **Testing:** Ready for endpoint testing and user flow validation

---

## Next Session Preview
**Day 2 Objectives:**
- Complete Meta Portal frontend (HTML/CSS/JavaScript)
- Test complete user registration and login flow
- Seed database with sample job data
- Add job listing and application endpoints
- Start Amazon Portal with React setup
- Establish automated testing foundation

---

## Day 2: August 1, 2025 (3 Hours Available)

### Hour 5: Complete Meta Portal [PLANNED]
**Time:** 1 hour | **Status:** ⏳ PLANNED
### Objectives:
- [ ] **Complete Meta Backend** (30 min)
  - Application submission endpoint
  - User profile management
  - Error handling and validation
  - Sample data population

- [ ] **Complete Meta Frontend** (20 min)
  - Job application form
  - Profile page
  - Success/error message handling
  - Navigation between pages

- [ ] **Testing & Validation** (10 min)
  - Manual testing of all flows
  - API testing with sample data
  - Cross-browser compatibility check

### Hour 6: Amazon Portal Setup [PLANNED]
**Time:** 1 hour | **Status:** ⏳ PLANNED
### Objectives:
- [ ] **Enhanced Backend** (40 min)
  - Extended user model (address, LinkedIn)
  - Work experience and education models
  - Enhanced application with "Why Amazon"
  - Multiple form sections handling

- [ ] **React Frontend Setup** (20 min)
  - Create React App initialization
  - Material-UI integration
  - Component structure setup
  - Routing configuration

### Hour 7: Testing & Documentation [PLANNED]
**Time:** 1 hour | **Status:** ⏳ PLANNED
### Objectives:
- [ ] **Cross-Portal Testing** (30 min)
  - Test user flows across portals
  - Data isolation verification
  - API endpoint validation

- [ ] **Automation Setup** (20 min)
  - Basic Selenium/Playwright setup
  - Simple test cases for registration/login
  - Test data management

- [ ] **Documentation & Commit** (10 min)
  - Update progress tracking
  - Commit all implementation
  - Prepare for next phase

**Ready to start Meta Portal implementation! Let's create the folder structure first.**


---
**Add-on Progress (August 1, 2025):**
- [x] Database models for User, Job, and Application completed and explained
- [x] Database connection setup with SQLAlchemy and SQLite
- [ ] Next: Table creation, schemas, and API endpoints

---

2a. Database Table Creation (5 min)
  - Use SQLAlchemy's Base.metadata.create_all(engine) to create tables in meta.db
  - Verify tables: users, jobs, applications

2b. Pydantic Schemas & Data Validation (10 min)
  - Define Pydantic models for User, Job, Application (request/response validation)
  - Ensure password hashing and phone validation in registration schema

2c. Authentication Service (10 min)
  - FastAPI app: user registration endpoint (POST /api/register)
  - Login endpoint (POST /api/login) with JWT token generation
  - Integrate bcrypt for password hashing
  - Enforce phone number as required field

2d. Basic Job Endpoints (5 min)
  - Job listing endpoint (GET /api/jobs)
  - Job details endpoint (GET /api/jobs/{id})
  - Seed database with 5-10 sample Meta jobs

---
### Backend/Frontend Integration Steps
1. Start FastAPI backend: `uvicorn main:app --reload`
2. Confirm endpoints are live at http://localhost:8000/docs
3. Build registration page: POST to /api/register
4. Build login page: POST to /api/login, store JWT token
5. Test full flow: register, login, receive token, and use for authenticated requests
---

Step 3: Frontend Foundation (15 minutes)
3a. Registration Page (5 min)
  - HTML form: email, password, first name, last name, phone (all required)
  - Client-side validation for all fields
  - Integrate with registration API, handle errors

3b. Login Page (5 min)
  - Login form: email and password
  - Store JWT token in localStorage after login
  - Redirect to jobs page on successful login
Redirect to jobs page after login
3c. Jobs Page (5 min)
Display job cards from API
Basic CSS styling
Apply button (leads to application form)

---

## Next Phase: UI/UX Revamp & Design Enhancement

### Overview
Complete redesign of all frontend pages with professional, modern UI using pastel purple/lavender color scheme and center-aligned layouts.

### Priority: HIGH
**Objective:** Transform the basic functional UI into a professional, visually appealing job portal

---

### Feature 1: Homepage/Main Page Enhancement
**Status:** ⏳ PLANNED

**Requirements:**
- Create professional landing page with hero banner section
- Add portal description and value proposition text
  - What the portal offers (job searching/posting)
  - Call-to-action messaging for users and employers
- Center-aligned, modern layout with proper spacing
- Clear CTA buttons for "Register" and "Login"
- Navigation menu for all portal features
- Responsive design for all screen sizes

**Design Elements:**
- Hero banner with background image or gradient
- Feature highlights section
- Testimonials or statistics (optional)
- Footer with links

---

### Feature 2: Jobs Page Redesign
**Status:** ⏳ PLANNED

**Requirements:**
- Redesign job listing cards with better visual hierarchy
  - Company logo placeholder
  - Job title, location, department prominently displayed
  - Salary range and job type badges
  - Brief description preview
- Proper grid/list view with consistent spacing
- Enhanced job details modal or dedicated page
- Add filtering/search UI elements:
  - Search bar
  - Department filter
  - Location filter
  - Job type filter
- Pagination controls
- Center-aligned content with responsive grid

**Design Elements:**
- Card-based layout with hover effects
- Filter sidebar or top bar
- Sort options (newest, salary, etc.)
- "No results" state design

---

### Feature 3: Registration Page Revamp
**Status:** ⏳ PLANNED

**Requirements:**
- Professional, center-aligned form layout
- Proper field grouping (Personal Info, Contact Info, etc.)
- Form validation with visual feedback
  - Real-time validation indicators
  - Error messages below each field
  - Success checkmarks for valid fields
- Clear success/error message styling with animations
- Progress indicator if multi-step registration
- "Already have an account? Login" link
- Responsive form design

**Design Elements:**
- Form container with shadow/elevation
- Floating labels or clear label positioning
- Password strength indicator
- Terms and conditions checkbox
- Submit button with loading state

---

### Feature 4: Login Page Redesign
**Status:** ⏳ PLANNED

**Requirements:**
- **CRITICAL FIX:** Center-align login form (currently too far left)
- Professional input field styling
- "Forgot password?" link with proper styling
- "Remember me" checkbox
- Clear error/success message presentation
- "Don't have an account? Register" link
- Social login placeholders (for future)
- Responsive design

**Design Elements:**
- Login container centered vertically and horizontally
- Icon-enhanced input fields (email icon, password icon)
- Submit button with hover effects
- Divider for alternative login methods
- Background design matching theme

---

### Global Design System

**Color Theme:**
- **Primary Palette:** Pastel purple/lavender/violet soft colors
- **Approach:** Use shades and tints to distinguish different UI elements
  - Primary buttons: Medium lavender
  - Secondary buttons: Light purple
  - Accent elements: Deeper violet
  - Backgrounds: Very light lavender tints
  - Text: Dark purple for headers, gray-purple for body

**Styling Implementation Strategy:**
- **Option 1:** Bootstrap theme customization
  - Use Bootstrap's CSS variables/SCSS to override default colors
  - Customize with pastel purple variants
- **Option 2:** Pre-built Bootstrap theme as base
  - Use Bootswatch themes (e.g., "Minty" or "Flatly") as starting point
  - Override with custom pastel purple palette
- **Option 3:** Custom CSS with Bootstrap components
  - Keep Bootstrap grid and components
  - Write custom CSS for color scheme and layouts

**Consistent Elements Across All Pages:**
- Navigation bar with consistent styling
- Footer with links and branding
- Button styles (primary, secondary, success, danger)
- Form input styling
- Card/container styling
- Loading spinners and animations
- Error/success message alerts
- Modal styling
- Spacing and typography scale

**Layout Principles:**
- Center-aligned main content
- Maximum content width with padding
- Responsive breakpoints for mobile/tablet/desktop
- Consistent padding and margins
- Professional background (subtle pattern or gradient)

---

### Implementation Checklist

**Phase 1: Setup & Design System (1-2 hours)**
- [ ] Choose and set up Bootstrap theme (custom or preset)
- [ ] Define CSS variables for color palette
- [ ] Create base styles for common components
- [ ] Set up typography scale
- [ ] Create reusable CSS classes

**Phase 2: Homepage (2-3 hours)**
- [ ] Create hero section HTML/CSS
- [ ] Add portal description content
- [ ] Implement CTA buttons
- [ ] Create features/benefits section
- [ ] Add footer
- [ ] Test responsive layout

**Phase 3: Login Page (1-2 hours)**
- [ ] Restructure HTML for center alignment
- [ ] Apply new form styling
- [ ] Add input icons
- [ ] Style buttons and links
- [ ] Test responsive design

**Phase 4: Registration Page (2-3 hours)**
- [ ] Restructure form layout
- [ ] Implement field validation UI
- [ ] Add success/error messaging
- [ ] Style all form elements
- [ ] Test validation flow
- [ ] Test responsive design

**Phase 5: Jobs Page (3-4 hours)**
- [ ] Redesign job card component
- [ ] Implement grid layout
- [ ] Add filter/search UI
- [ ] Create job details view
- [ ] Add pagination controls
- [ ] Test interactions and responsive design

**Phase 6: Testing & Polish (1-2 hours)**
- [ ] Cross-browser testing
- [ ] Mobile responsiveness testing
- [ ] Accessibility checks
- [ ] Performance optimization
- [ ] Final visual polish

---

### Success Criteria
- All pages use consistent pastel purple color scheme
- All layouts are center-aligned and responsive
- Login form is properly centered (not left-aligned)
- Job cards have modern, professional appearance
- Forms have clear validation and feedback
- Homepage has engaging content and clear CTAs
- All pages work on mobile, tablet, and desktop
- Loading states and transitions are smooth
- Overall design looks professional and cohesive

---

**Estimated Total Time:** 10-16 hours
**Priority:** HIGH - Foundation for user experience
**Dependencies:** None (can start immediately)

---

## v1.1.0 Unified Feature Roadmap
*Professional UI + Realistic Functionality + Automation Testing Ready*

---

### **PHASE 1: Foundation & Visual Identity** (Priority: CRITICAL)
*Establish professional look and core design system*

#### **Feature 1.1: Global Design System Setup**
**Description:** Implement pastel purple/lavender color scheme across entire site

**Implementation:**
- Bootstrap theme customization (CSS variables/SCSS)
- Define color palette (primary, secondary, accent, backgrounds)
- Create reusable component styles (buttons, cards, forms, modals)
- Set up typography scale
- Establish spacing/layout standards

**Automation Benefit:** Consistent class names and structure from the start  
**Time Estimate:** 2-3 hours

#### **Feature 1.2: Homepage/Landing Page Enhancement**
**Description:** Professional entry point with hero banner and clear value proposition

**UI/UX Elements:**
- Hero section with background gradient/image
- Portal description ("Find your dream job" messaging)
- Feature highlights section
- Clear CTAs for Register/Login
- Navigation bar with all sections
- Footer with links

**Functional Elements:**
- Responsive layout (mobile/tablet/desktop)
- Smooth scroll navigation
- Loading states

**Automation Benefit:** Complex landing page with multiple sections to test  
**Time Estimate:** 3-4 hours

---

### **PHASE 2: Authentication & User Experience** (Priority: HIGH)
*Fix existing pages with professional styling*

#### **Feature 2.1: Registration Page Revamp**
**Description:** Professional, center-aligned registration with validation

**UI/UX Elements:**
- Center-aligned form container with shadow
- Field grouping (Personal Info, Contact Info)
- Floating labels or clear positioning
- Password strength indicator
- Visual validation feedback (checkmarks, error messages)
- Success/error toast notifications
- "Already have account?" link

**Functional Elements:**
- Real-time client-side validation
- Terms & conditions checkbox
- Submit button loading state

**Automation Benefit:** Multiple input types, validation states, dynamic feedback  
**Time Estimate:** 2-3 hours

#### **Feature 2.2: Login Page Redesign**
**Description:** Center-aligned professional login (fix current left-alignment issue)

**UI/UX Elements:**
- **CRITICAL FIX:** Center vertically and horizontally
- Icon-enhanced input fields
- "Remember me" checkbox
- "Forgot password?" link
- "Don't have account?" register link
- Clear error messaging

**Functional Elements:**
- JWT token handling
- Session management
- Error state handling

**Automation Benefit:** Simple form with multiple interactive elements  
**Time Estimate:** 1-2 hours

---

### **PHASE 3: Core Job Portal Features** (Priority: HIGH)
*Main functionality with professional UI*

#### **Feature 3.1: Jobs Page Redesign + Search & Filter**
**Description:** Modern job listing with search and filtering capabilities

**UI/UX Elements:**
- Card-based layout with hover effects
- Grid view with consistent spacing
- Professional job card design:
  - Company logo placeholder
  - Job title, location, department badges
  - Salary range display
  - Brief description preview
  - "Apply" button with styling

**Functional Elements:**
- Search by keyword (job title, description)
- Filter by:
  - Location dropdown
  - Department dropdown
  - Job type (Full-time, Part-time, Contract)
- Sort options: Newest, Salary (High-Low), Relevance
- Clear/Reset filters button

**Automation Benefit:** Dynamic DOM updates on filter changes, multiple locator types  
**Time Estimate:** 4-5 hours

#### **Feature 3.2: Job Details Page/Modal**
**Description:** Detailed view when clicking on a job card

**UI/UX Elements:**
- Full-screen modal or dedicated page
- Professional layout with all job information
- Styled sections (Description, Requirements, Benefits)
- Prominent "Apply" button

**Functional Elements:**
- Opens on job card click
- Displays full job description
- Shows requirements list
- Application form integration
- Close/back navigation

**Automation Benefit:** Modal toggles, nested locators, dynamic waits  
**Time Estimate:** 2-3 hours

#### **Feature 3.3: Pagination & Lazy Loading**
**Description:** Load jobs in chunks for performance and testing

**Functional Elements:**
- Option 1: "Load More" button
- Option 2: Infinite scroll (IntersectionObserver)
- Show "Loading..." state
- Track current page/offset

**Automation Benefit:** Element reloading, stale element exceptions, scroll testing  
**Time Estimate:** 2-3 hours

---

### **PHASE 4: User Dashboard & Profile** (Priority: MEDIUM-HIGH)
*Post-login experience*

#### **Feature 4.1: Candidate Dashboard**
**Description:** User's home after login showing application history

**UI/UX Elements:**
- Welcome message with user name
- Dashboard card layout
- Statistics (applications submitted, pending, etc.)
- Quick actions section

**Functional Elements:**
- View all applied jobs with status
- Application status badges:
  - "Applied" (blue)
  - "In Review" (yellow)
  - "Rejected" (red)
  - "Interview Scheduled" (green)
- Filter by status
- Sort by date applied
- Link to each job details

**Automation Benefit:** Dynamic state changes, backend-driven updates  
**Time Estimate:** 3-4 hours

#### **Feature 4.2: User Profile Section**
**Description:** Edit personal information and preferences

**UI/UX Elements:**
- Tabbed interface (Personal Info, Experience, Skills)
- Form with editable fields
- Avatar/photo upload placeholder
- Save button with confirmation

**Functional Elements:**
- Update name, email, phone
- Add/edit skills (tags)
- Update bio/summary
- Form validation

**Automation Benefit:** Multiple form field types (input, textarea, dropdown, tags)  
**Time Estimate:** 2-3 hours

---

### **PHASE 5: Admin/HR Portal** (Priority: MEDIUM)
*Management side of the portal*

#### **Feature 5.1: Admin/HR Dashboard**
**Description:** Separate admin interface with elevated permissions

**UI/UX Elements:**
- Different layout/color scheme (distinguish from candidate view)
- Admin navigation sidebar
- Dashboard with analytics cards
- Data tables with actions

**Functional Elements:**
- Admin login (separate route or role check)
- View all applicants in table format
- Filter/search applicants
- View application details
- Change application status (approve/reject)
- User management section

**Automation Benefit:** Role-based testing, different UI layouts, permission checks  
**Time Estimate:** 4-5 hours

#### **Feature 5.2: Job Management (Admin)**
**Description:** CRUD operations for jobs

**Functional Elements:**
- Create new job posting (form)
- Edit existing jobs
- Delete jobs (with confirmation)
- Toggle job active/inactive status
- View applicants per job

**Automation Benefit:** Full CRUD testing, form submission, confirmation modals  
**Time Estimate:** 3-4 hours

#### **Feature 5.3: Admin Analytics Dashboard** (Optional)
**Description:** Simple metrics and charts

**Functional Elements:**
- Number of total applicants
- Number of jobs posted
- Application status breakdown (chart)
- Recent activity feed

**Automation Benefit:** Chart elements (SVGs), dynamic numbers, data visualization testing  
**Time Estimate:** 2-3 hours

---

### **PHASE 6: Enhanced UX Features** (Priority: MEDIUM)
*Polish and user convenience*

#### **Feature 6.1: Notifications System**
**Description:** Toast messages for user actions

**Functional Elements:**
- "Application Submitted" success message
- "Status Updated" notification
- "Job Posted" confirmation
- "Error occurred" alerts

**UI/UX Elements:**
- Toast appears at top-right or top-center
- Auto-dismiss after 3-5 seconds
- Different colors for success/error/info
- Smooth animations

**Automation Benefit:** Timing challenges, visibility testing, wait-for-disappear logic  
**Time Estimate:** 2-3 hours

#### **Feature 6.2: Application Status Flow**
**Description:** End-to-end status update system

**Functional Elements:**
- HR changes status in admin panel
- Candidate sees updated status on dashboard
- Email notification (optional/simulated)
- Status history log

**Automation Benefit:** Backend-driven DOM changes, real-time updates  
**Time Estimate:** 2-3 hours

#### **Feature 6.3: Responsive Layouts**
**Description:** Mobile-first responsive design

**Functional Elements:**
- Collapse navigation on mobile (hamburger menu)
- Stack job cards vertically on small screens
- Hide/show elements based on viewport (d-none, d-md-block)
- Touch-friendly buttons and spacing

**Automation Benefit:** Viewport-based DOM shifts, responsive testing  
**Time Estimate:** 3-4 hours (across all pages)

---

### **PHASE 7: Automation Testing Enhancements** (Priority: MEDIUM-LOW)
*Features specifically for test automation framework*

#### **Feature 7.1: Dynamic Behaviors / Chaos Mode**
**Description:** Controlled DOM instability for self-healing testing

**Functional Elements:**
- Backend flag: `CHAOS_MODE = True/False`
- Randomized IDs: Element IDs change on page load
- Attribute Drift: Class names randomly renamed
- Text Variation: Button text alternates ("Apply" ↔ "Submit")
- Layout Switch: Toggle grid/list view randomly
- Dynamic Delays: Random 1-3 sec rendering delays
- Modal Re-rendering: Recreate modal HTML on each open
- Random Reordering: Shuffle job card order
- Implementation: Backend middleware or JS config

**Automation Benefit:** Train self-healing locators, simulate real-world drift  
**Time Estimate:** 4-6 hours

#### **Feature 7.2: Locator Metadata API**
**Description:** Real-time tracking of element locators

**Functional Elements:**
- API endpoint: `GET /api/locators/logs`
- Returns JSON: `{element_name: current_locator}`
- Middleware updates JSON when IDs mutate
- Log all locator changes with timestamp

**Automation Benefit:** AI can fetch real-time locator changes for benchmarking  
**Time Estimate:** 2-3 hours

#### **Feature 7.3: Semantic Label Mapping**
**Description:** Ground-truth validation attributes

**Functional Elements:**
- Add `data-ai-label="apply_button"` to all key elements
- Hidden from frontend styling
- Never changes (stable reference)
- Maps to functional purpose

**Automation Benefit:** AI can validate if recovered locator matched correct element  
**Time Estimate:** 1-2 hours (add to existing elements)

#### **Feature 7.4: DOM Snapshots & Version Control**
**Description:** Save HTML structure for comparison

**Functional Elements:**
- Capture rendered HTML of critical pages
- Store as `.html` files with version/timestamp
- Compare old vs new DOMs
- Highlight structural changes

**Automation Benefit:** Train similarity engine, track DOM evolution  
**Time Estimate:** 2-3 hours

#### **Feature 7.5: Recovery Visualization Dashboard**
**Description:** Internal debug page showing self-healing metrics

**Functional Elements:**
- Route: `/debug/selfheal`
- Show diff of original vs recovered locators
- Heatmap of healing success rate
- List of all mutations and recoveries
- Performance metrics

**Automation Benefit:** Portfolio showcase, real-time monitoring  
**Time Estimate:** 3-4 hours

#### **Feature 7.6: Performance Feedback API**
**Description:** Endpoint for AI framework to report results

**Functional Elements:**
- API endpoint: `POST /api/testfeedback/`
- Receive: healed locator, success rate, retry count
- Store in database
- Generate reports

**Automation Benefit:** Evaluate AI healing performance in real-time  
**Time Estimate:** 2-3 hours

#### **Feature 7.7: Error Simulation Switch**
**Description:** Intentionally break locators for testing

**Functional Elements:**
- Backend endpoint: `POST /simulate/error`
- Parameters: element_name, error_type
- Temporarily mutate specific element
- Reset after test

**Automation Benefit:** Controlled testing of recovery mechanisms  
**Time Estimate:** 1-2 hours

#### **Feature 7.8: Element Mutation Log**
**Description:** Track all locator changes

**Functional Elements:**
- Log before/after mapping when elements mutate
- Store in JSON file or database
- Include timestamp, element, old locator, new locator
- Export as dataset

**Automation Benefit:** Labeled dataset for training recovery accuracy  
**Time Estimate:** 2-3 hours

#### **Feature 7.9: System Logs / Debug Page**
**Description:** Hidden internal route for debugging

**Functional Elements:**
- Route: `/debug/locators`
- Show all current element locators
- Real-time updates
- Export/copy functionality

**Automation Benefit:** Quick reference for test development  
**Time Estimate:** 1-2 hours

---

## **Summary by Priority**

### **Must Have (Critical Path - 25-35 hours):**
1. Global Design System Setup
2. Homepage Enhancement
3. Registration Page Revamp
4. Login Page Redesign
5. Jobs Page + Search & Filter
6. Job Details Page
7. Candidate Dashboard
8. Admin Dashboard
9. Job Management (Admin)

### **Should Have (Important - 15-20 hours):**
10. Pagination & Lazy Loading
11. User Profile Section
12. Notifications System
13. Application Status Flow
14. Responsive Layouts
15. Chaos Mode Implementation

### **Nice to Have (Enhancement - 15-20 hours):**
16. Admin Analytics
17. Locator Metadata API
18. Semantic Label Mapping
19. DOM Snapshots
20. Recovery Visualization Dashboard
21. Performance Feedback API
22. Error Simulation
23. Element Mutation Log
24. System Logs/Debug Page

---

## **Total Estimated Time: 55-75 hours**

---

## **Implementation Strategy**

1. **Weeks 1-2:** Phase 1-3 (Foundation + Core Features) → Get site looking professional
2. **Weeks 3-4:** Phase 4-5 (Dashboards + Admin) → Add realistic functionality
3. **Week 5:** Phase 6 (Enhanced UX) → Polish user experience
4. **Week 6-7:** Phase 7 (Automation Features) → Add self-healing capabilities