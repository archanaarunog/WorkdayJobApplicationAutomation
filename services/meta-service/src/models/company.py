"""
Company model for Meta Portal - Multi-Tenancy Support.

This defines the structure for companies in our multi-tenant system.
Each company has its own isolated data and admin users.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.config.database import Base

class Company(Base):
    """
    Company table definition.
    Each company represents a separate tenant with isolated data.
    """
    __tablename__ = "companies"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Company information
    name = Column(String(200), nullable=False, unique=True, index=True)
    domain = Column(String(100), nullable=True, unique=True, index=True)  # company domain (e.g., meta.com)
    slug = Column(String(50), nullable=False, unique=True, index=True)  # URL-friendly identifier
    
    # Company details
    description = Column(Text, nullable=True)
    industry = Column(String(100), nullable=True)
    website = Column(String(255), nullable=True)
    headquarters = Column(String(200), nullable=True)
    size = Column(String(50), nullable=True)  # Small, Medium, Large, Enterprise
    
    # Company settings (stored as JSON for flexibility)
    settings = Column(JSON, nullable=True, default={
        'job_posting_approval_required': False,
        'allow_external_applications': True,
        'email_notifications': True,
        'branding_color': '#007bff',
        'logo_url': None,
        'custom_application_fields': []
    })
    
    # Admin user (the primary admin who can manage the company)
    admin_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # Status and timestamps
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    # All users belonging to this company
    users = relationship("User", back_populates="company", foreign_keys="User.company_id")
    
    # All jobs posted by this company
    jobs = relationship("Job", back_populates="company", cascade="all, delete-orphan")
    
    # All applications for jobs at this company
    applications = relationship("Application", back_populates="company", cascade="all, delete-orphan")
    
    # The admin user relationship (separate from general users)
    admin_user = relationship("User", foreign_keys=[admin_user_id], post_update=True)

    def __repr__(self):
        return f"<Company(id={self.id}, name='{self.name}', domain='{self.domain}', active={self.is_active})>"
    
    @property
    def user_count(self):
        """Get the total number of users in this company."""
        return len(self.users)
    
    @property
    def job_count(self):
        """Get the total number of jobs posted by this company."""
        return len(self.jobs)
    
    @property
    def application_count(self):
        """Get the total number of applications for this company's jobs."""
        return len(self.applications)
    
    @property
    def active_job_count(self):
        """Get the number of active jobs for this company."""
        return len([job for job in self.jobs if job.is_active])