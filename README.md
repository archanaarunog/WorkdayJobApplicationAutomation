

# Meta Portal Job Application System (V1.1.0 - In Progress)

**Project Title:** Meta Portal Job Application System

**Description:**
This project is a realistic, end-to-end job application portal designed for SDET/SDE learning and portfolio building. It features a FastAPI backend, SQLAlchemy ORM, JWT authentication, and a modern Bootstrap-styled frontend with custom purple/lavender theme. The system demonstrates secure user registration/login, job listing, and a functional job application workflow with modal forms.

**Latest Updates (v1.1.0):**
- ✨ Custom pastel purple/lavender design system implemented
- 🎨 Professional UI/UX with centered forms, shadow effects, and hover animations
- 📐 Consistent typography and spacing across all pages
- 🔧 Enhanced form styling with purple focus states and labels

---

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

### v1.1.0 (In Progress - Phase 1 Complete)
**Design System & UI/UX Improvements:**
- ✅ Created global theme.css with CSS custom properties
- ✅ Implemented pastel purple/lavender color scheme (#9B8ACB primary, #E2D9F3 light backgrounds)
- ✅ Updated all buttons with purple styling and hover effects
- ✅ Enhanced card components with shadows and hover animations
- ✅ Improved form inputs with purple focus states and proper labeling
- ✅ Added consistent typography classes (heading-1, heading-2, heading-3, text-body, text-small)
- ✅ Implemented proper spacing and padding across all pages
- ✅ Centered login/register forms with professional layout
- ✅ Added background pattern with gradient effects
- ✅ Applied theme consistently across index, login, register, and jobs pages

**File Changes:**
- Created: `frontend/meta-ui/public/assets/css/theme.css` (340+ lines)
- Modified: All HTML files (index, login, register, jobs) with new classes and styling
- Modified: `frontend/meta-ui/assets/js/jobs.js` for enhanced card rendering

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
