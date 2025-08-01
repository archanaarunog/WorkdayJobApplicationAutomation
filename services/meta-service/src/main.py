"""
Main FastAPI application for Meta Portal.

This is the entry point for our backend server.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config.database import engine, Base
from .models import user, job, application

# Create all database tables
# This reads our model definitions and creates the actual tables
Base.metadata.create_all(bind=engine)

# Create the FastAPI application
app = FastAPI(
    title="Meta Portal API",
    description="Job Application Portal for Meta",
    version="1.0.0"
)

# Add CORS middleware to allow frontend to communicate with backend
# CORS = Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Allow all headers
)

# Basic health check endpoint
@app.get("/")
async def root():
    """
    Health check endpoint.
    This confirms our server is running.
    """
    return {"message": "Meta Portal API is running!", "status": "healthy"}

@app.get("/health")
async def health_check():
    """
    Detailed health check for system monitoring.
    """
    return {
        "status": "healthy",
        "service": "meta-portal",
        "version": "1.0.0"
    }

# We'll add more endpoints here as we build them
# The routes will be imported and included here
