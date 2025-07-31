# System Architecture - Job Applicat**Explanation:**  
- JAPS Main Portal is the central aggregator, fetching job data from all company portals via API calls.
- Meta, Amazon, and Google Portals are independent, each with its own frontend, backend, and database.
- Each portal runs on a different port and maintains its own SQLite database for user, job, and application data.
- No direct data sharing between company portals—each is isolated, just like real-world companies.

---

## 3. Data Flow Architecture

### User Journey & Data Movement

1. **Job Discovery**
   - User visits JAPS Main Portal.
   - JAPS Main fetches job listings from Meta, Amazon, and Google portals via API calls (e.g., `/api/jobs`).
   - User browses, filters, and searches jobs from all companies in one place.

2. **Application Initiation**
   - User clicks "Apply" on a job in JAPS Main.
   - JAPS Main redirects the user to the selected company portal (e.g., Amazon Portal).
   - No user data is transferred—only the job reference or ID may be passed in the URL.

3. **Registration/Login**
   - User registers or logs in on the company portal (Meta, Amazon, or Google).
   - User credentials and profile data are stored only in that portal's database.

4. **Profile & Application Submission**
   - User fills out profile and application forms on the company portal.
   - Data is saved in the company portal's database (e.g., `amazon.db`).
   - Resume upload and parsing (Google only) handled locally in that portal.

5. **Confirmation & Status Tracking**
   - User receives on-screen confirmation or simulated email.
   - Application status is tracked only in the company portal's system.em (JAPS)

## 1. System Overview

The Job Application Portal System (JAPS) is a multi-portal mock ecosystem designed to simulate real-world job application workflows across multiple company platforms. It consists of a central job aggregator (JAPS Main) and three independent company portals (Meta, Amazon, Google), each with its own backend, frontend, and database. The system is built for automation testing, learning, and portfolio demonstration, following a microservices-inspired, containerized architecture.

**Key Goals:**
- Demonstrate automation of job applications across diverse platforms
- Simulate realistic company separation (data, authentication, workflows)
- Enable cross-portal navigation and automation testing
- Showcase scalable, modular, and industry-standard architecture

---

## 2. Component Diagram


```
                        ┌─────────────────────────────┐
                        │      JAPS Main Portal       │
                        │  (React + FastAPI, :3000)   │
                        └─────────────┬───────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
┌───────▼───────┐             ┌───────▼───────┐             ┌───────▼───────┐
│   Meta Portal │             │ Amazon Portal │             │ Google Portal  │
│ (HTML+FastAPI)│             │ (React+FastAPI)│            │ (React+FastAPI)│
│   (:3001)     │             │   (:3002)     │             │   (:3003)      │
└───────┬───────┘             └───────┬───────┘             └───────┬───────┘
        │                             │                             │
 ┌──────▼─────┐                ┌──────▼─────┐                ┌──────▼─────┐
 │ meta.db    │                │ amazon.db  │                │ google.db  │
 └────────────┘                └────────────┘                └────────────┘
```

**Explanation:**  
- No direct data sharing between company portals—each is isolated, just like real-world companies.
### User Journey & Data Movement

1. **Job Discovery**
   - User visits JAPS Main Portal.
   - JAPS Main fetches job listings from Meta, Amazon, and Google portals via API calls (e.g., `/api/jobs`).
   - User browses, filters, and searches jobs from all companies in one place.

   - No user data is transferred—only the job reference or ID may be passed in the URL.

4. **Profile & Application Submission**
   - User fills out profile and application forms on the company portal.
5. **Confirmation & Status Tracking**
   - Application status is tracked only in the company portal’s system.

### Portal Isolation
- Each portal maintains its own user, job, and application data in a separate SQLite database.
- No direct data sharing or synchronization between company portals.
- Users must register separately on each portal if applying to multiple companies.

### Automation Testing Hooks
- Automation scripts can:
  - Simulate job search and filtering on JAPS Main
  - Click “Apply” and verify redirection to the correct portal
  - Register/login, fill forms, upload resumes, and submit applications on each portal
  - Validate confirmation messages and application status
- End-to-end tests should cover the full journey for each company portal independently.

---

## 4. Service Communication & APIs


### Overview
All communication between portals is via RESTful APIs. There is no direct database or session sharing. JAPS Main Portal acts as the aggregator, making API calls to each company portal to fetch job data. Each company portal exposes its own set of endpoints for job listings, user management, and application processing.

### Key API Interactions

1. **Job Aggregation (JAPS Main → Company Portals)**
   - JAPS Main calls:
     - `GET /api/jobs` on Meta, Amazon, and Google portals to retrieve job listings.
   - Response: List of jobs (title, company, location, salary, job ID, etc.)

2. **User Actions (Company Portals)**
   - Registration: `POST /api/register` (Meta, Amazon, Google)
   - Login: `POST /api/login`
   - Profile: `GET/POST /api/profile`
   - Application Submission: `POST /api/apply` (with job ID and user data)
3. **Redirection**
   - JAPS Main redirects user to the selected company portal with job reference (e.g., `/apply?job_id=123`)
   - No sensitive data is passed in the URL.

### API Security & Standards
- JWT tokens are used for authentication within each portal (no cross-portal sessions).
- OpenAPI/Swagger documentation is provided for each backend.
- Input validation and error handling are enforced at the API level.

### API Security & Standards
- All APIs use JSON for request/response.
- JWT tokens are used for authentication within each portal (no cross-portal sessions).
- OpenAPI/Swagger documentation is provided for each backend.
- Input validation and error handling are enforced at the API level.

### Automation Testing Hooks
- API endpoints can be tested directly for functional and integration testing.
- End-to-end automation scripts interact with these APIs via the UI or directly for advanced scenarios.

---

## 5. Database Architecture

### Overview
Each portal maintains its own isolated SQLite database. This mirrors real-world company separation and supports realistic automation testing scenarios.

### Database per Portal
- **JAPS Main:** `japs_main.db` (companies, aggregated jobs)
- **Meta Portal:** `meta.db` (users, jobs, applications)
- **Amazon Portal:** `amazon.db` (users, jobs, applications)
- **Google Portal:** `google.db` (users, jobs, applications, resumes)

### Key Tables (per company portal)
- `users`: Stores user registration and profile data
- `jobs`: Stores job postings for that company
- `applications`: Stores job applications submitted by users
- `sessions`: (optional) For session management/JWT tracking
- `resumes`: (Google only) Stores uploaded resume metadata

### Data Isolation & Security
- No data is shared between databases or portals.
- Each portal is responsible for its own data integrity, validation, and backup.
- This design supports realistic automation testing, as each portal can be reset or modified independently.

### Automation Testing Hooks
- Databases can be pre-populated with test data for repeatable automation runs.
- Data can be validated after test runs to ensure correct application state.

---

## 6. Docker & Deployment Strategy


### Overview
All portals and services are containerized using Docker, allowing for consistent, reproducible local development and testing. Docker Compose orchestrates the startup of all services, ensuring each portal runs on its own port with isolated dependencies and databases.

### Key Points
- **Dockerfiles:** Each portal (JAPS Main, Meta, Amazon, Google) has its own Dockerfile for backend and frontend (if applicable).
- **Docker Compose:** A single `docker-compose.yml` file defines all services, networks, and volumes. Running `docker-compose up` starts the entire ecosystem.
- **Port Mapping:**
  - JAPS Main: `localhost:3000`
  - Meta: `localhost:3001`
  - Amazon: `localhost:3002`
  - Google: `localhost:3003`
- **Volume Mounts:** Databases are persisted as local files, making it easy to reset or inspect data.
- **Environment Variables:** Used for configuration (e.g., JWT secrets, DB paths) and can be managed via `.env` files.
- **Benefits:**
  - Consistent environment for all developers/testers
  - Easy to spin up/tear down the entire system
  - Supports automation and CI/CD pipelines

### Deployment Flow
1. Build Docker images for each service.
2. Start all services with Docker Compose.
3. Access each portal via its assigned port.
4. Run automation tests against the running containers.

---

## 7. Folder Structure & Code Organization

### Overview
The project uses a modular, microservices-inspired folder structure to separate concerns and support scalability. Each portal and service has its own directory for backend, frontend, and database files. Documentation, automation tests, and scripts are organized for clarity and ease of use.

### Example Structure

```
WorkdayJobApplicationAutomation/
├── docs/                                    # Documentation
│   ├── requirements_specification.md
│   ├── system_architecture.md
│   └── api_specifications.md
├── services/                               # All backend services
│   ├── japs-main-service/                 # Main portal backend
│   │   ├── src/
│   │   │   ├── main.py                    # FastAPI app
│   │   │   ├── models/                    # Database models
│   │   │   ├── routes/                    # API endpoints
│   │   │   └── database/                  # DB connection
│   │   ├── requirements.txt
│   │   └── Dockerfile
│   ├── meta-service/                      # Meta portal backend
│   ├── amazon-service/                    # Amazon portal backend
│   └── google-service/                    # Google portal backend
├── frontend/                              # All frontend apps
│   ├── japs-main-ui/                     # Main portal (React)
│   ├── meta-ui/                          # Meta portal (HTML/CSS)
│   ├── amazon-ui/                        # Amazon portal (React)
│   └── google-ui/                        # Google portal (React)
├── databases/                             # SQLite files
│   ├── japs_main.db
│   ├── meta.db
│   ├── amazon.db
│   └── google.db
├── automation-tests/                      # Test automation
│   ├── selenium/
│   ├── playwright/
│   └── api-tests/
├── docker-compose.yml                     # Orchestration
├── .github/workflows/                     # CI/CD
└── scripts/                              # Setup scripts
    ├── setup.sh
    └── start-all.sh
```

### Best Practices
- Keep each portal/service self-contained for easy development and testing.
- Use clear naming conventions and documentation in each directory.
- Store test data and automation scripts separately for maintainability.
- Use version control (Git) for all code, configs, and documentation.

---

## 8. Scalability & Extensibility Notes

### Overview
The architecture is designed for easy scaling and future enhancements. New company portals, features, or integrations can be added with minimal disruption to existing services.

### Scalability
- **Add New Portals:** Simply create a new service directory, Dockerfile, and database. Update Docker Compose and JAPS Main to recognize the new portal.
- **Horizontal Scaling:** Each portal can be containerized and scaled independently if needed (e.g., for load testing).
- **Automation Scaling:** Automation tests can be extended to cover new portals or features without affecting existing flows.

### Extensibility
- **Feature Additions:** New features (e.g., advanced resume parsing, analytics) can be added to individual portals without impacting others.
- **API Expansion:** REST APIs can be extended with new endpoints as requirements grow.
- **Cloud Migration:** The system can be migrated to cloud platforms (e.g., AWS ECS, Azure Container Apps) with minimal changes due to containerization.
- **CI/CD Integration:** The modular structure supports automated builds, tests, and deployments for each service.

### Portfolio & Learning Value
- Demonstrates real-world, scalable system design
- Shows ability to work with microservices, containers, and automation
- Prepares for enterprise-level SDET/SDE roles

