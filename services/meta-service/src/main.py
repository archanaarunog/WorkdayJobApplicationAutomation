
# Main FastAPI application for Meta Portal.
# This is the entry point for our backend server.
#
# Flow:
# 1. Creates all database tables from your models (User, Job, Application).
# 2. Sets up the FastAPI app instance.
# 3. Adds CORS middleware so your frontend (React, etc.) can call the backend API.
# 4. Includes the user router, which enables /api/register and /api/login endpoints.
# 5. Adds a health check endpoint for server status.


# Import FastAPI and CORS middleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import database engine and Base for table creation
from src.config.database import engine, Base
# Import all models so tables are created
from src.models import user, job, application


# Import user, job, and application routers
from src.routes import user as user_routes
from src.routes import job as job_routes
from src.routes import applications as applications_routes


# Create all database tables from models (run once at startup)
# This reads your SQLAlchemy models and creates the tables in the database if they don't exist.
Base.metadata.create_all(bind=engine)


# Create the FastAPI app instance
# This is the main app object for your backend API.
app = FastAPI(
    title="Meta Portal API",
    description="Job Application Portal for Meta",
    version="1.0.0"
)


# Add CORS middleware to allow frontend (React, etc.) to call the backend API
# CORS (Cross-Origin Resource Sharing) lets your frontend (on a different port/domain) access the backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8080"
    ],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)




# Register the user, job, and application routers
app.include_router(user_routes.router)
app.include_router(job_routes.router)
app.include_router(applications_routes.router)


# Health check endpoint (optional, for testing server status)
# You can visit http://localhost:8000/ to check if the server is running.
@app.get("/")
def root():
    return {"message": "Meta Portal API is running!"}
