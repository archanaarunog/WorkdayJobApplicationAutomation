"""
Job model for Meta Portal.

This defines the structure of job postings in our database.
"""

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.sql import func
from src.config.database import Base

class Job(Base):
    """
    Job table definition.
    Each job posting will be stored as a row in this table.
    """
    __tablename__ = "jobs"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Job information
    title = Column(String(200), nullable=False, index=True)  # Indexed for searching
    department = Column(String(100), nullable=True)
    location = Column(String(100), nullable=False)
    job_type = Column(String(50), default="Full-time", nullable=False)  # Full-time, Part-time, Contract
    experience_level = Column(String(50), nullable=True)  # Entry, Mid, Senior
    
    # Salary information (stored as integers for easy filtering)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    
    # Job details (Text allows longer content than String)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    
    # Timestamps and status
    posted_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationship: All applications submitted for this job
    # This allows you to do: job.applications to get a list of Application objects
    # back_populates must match the name used in Application model's relationship to Job
    from sqlalchemy.orm import relationship
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Job(id={self.id}, title='{self.title}', location='{self.location}')>"
    



# class Job(Base):
#     __tablename__ = "jobs" # name of the table

#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)

#     title = Column(String(200), nullable=False, index=True)

#     department = Column(String(100), nullable=True)

#     location = Column(String(100), nullable=False)

#     job_type = Column(String(50), nullable=True, default="Full-time")

#     def __repr__(self):
#         return f"<Job(id={self.id})>"
