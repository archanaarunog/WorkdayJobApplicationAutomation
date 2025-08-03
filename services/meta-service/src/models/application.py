"""
Application model for Meta Portal.

This tracks job applications submitted by users.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.config.database import Base

class Application(Base):
    """
    Application table definition.
    Links users to jobs they've applied for.
    """
    __tablename__ = "applications"

    # Primary key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Foreign keys - these link to other tables
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    
    # Application content
    cover_letter = Column(Text, nullable=False)  # Required field
    additional_info = Column(Text, nullable=True)  # Optional field
    
    # Application status tracking
    status = Column(String(50), default="submitted", nullable=False)
    
    # Timestamps
    applied_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


    # Relationships - these help us easily access related data
    # back_populates links this relationship to the corresponding one in User and Job
    # This allows bidirectional access: application.user and user.applications
    user = relationship("User", back_populates="applications")
    # This allows bidirectional access: application.job and job.applications
    job = relationship("Job", back_populates="applications")

    def __repr__(self):
        return f"<Application(id={self.id}, user_id={self.user_id}, job_id={self.job_id}, status='{self.status}')>"


# CREATE  TABLE applications(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     FOREING KEY(user_id) REFERENCES users(id),

# )