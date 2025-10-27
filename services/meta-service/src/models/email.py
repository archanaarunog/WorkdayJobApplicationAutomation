from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base
import enum

class EmailStatus(enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"

class EmailPriority(enum.Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class Email(Base):
    """
    Email tracking and history model
    Stores all email communications sent through the system
    """
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    
    # Email Details
    recipient_email = Column(String(255), nullable=False, index=True)
    recipient_name = Column(String(255), nullable=True)
    sender_email = Column(String(255), nullable=False)
    sender_name = Column(String(255), nullable=True)
    subject = Column(String(500), nullable=False)
    html_content = Column(Text, nullable=True)
    text_content = Column(Text, nullable=True)
    
    # Template Information
    template_name = Column(String(100), nullable=True, index=True)
    template_data = Column(JSON, nullable=True)  # Variables used in template
    
    # Status and Processing
    status = Column(Enum(EmailStatus), default=EmailStatus.PENDING, nullable=False, index=True)
    priority = Column(Enum(EmailPriority), default=EmailPriority.NORMAL, nullable=False)
    
    # Timestamps
    scheduled_at = Column(DateTime, nullable=True)  # For delayed sending
    sent_at = Column(DateTime, nullable=True)
    delivered_at = Column(DateTime, nullable=True)  # If tracking is enabled
    opened_at = Column(DateTime, nullable=True)    # If tracking is enabled
    
    # Error Handling
    failed_reason = Column(Text, nullable=True)
    retry_count = Column(Integer, default=0, nullable=False)
    max_retries = Column(Integer, default=3, nullable=False)
    
    # Relationships
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=True, index=True)
    
    # Metadata
    tracking_enabled = Column(Boolean, default=False, nullable=False)
    tracking_id = Column(String(100), nullable=True, unique=True, index=True)
    external_message_id = Column(String(255), nullable=True)  # SMTP message ID
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    company = relationship("Company", back_populates="emails")
    user = relationship("User", foreign_keys=[user_id], back_populates="received_emails")
    creator = relationship("User", foreign_keys=[created_by])
    application = relationship("Application", back_populates="emails")
    job = relationship("Job", back_populates="emails")

    def __repr__(self):
        return f"<Email(id={self.id}, recipient='{self.recipient_email}', subject='{self.subject[:50]}...', status='{self.status.value}')>"

class EmailTemplate(Base):
    """
    Email template management model
    Stores reusable email templates with variable substitution
    """
    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, index=True)
    
    # Template Identity
    name = Column(String(100), nullable=False, unique=True, index=True)
    display_name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    
    # Template Content
    subject_template = Column(String(500), nullable=False)
    html_content = Column(Text, nullable=True)
    text_content = Column(Text, nullable=False)
    
    # Template Metadata
    variables = Column(JSON, nullable=True)  # List of required template variables
    category = Column(String(50), nullable=True, index=True)  # job, user, admin, system
    language = Column(String(10), default="en", nullable=False)
    
    # Company Customization
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=True, index=True)
    is_system_template = Column(Boolean, default=False, nullable=False)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    version = Column(Integer, default=1, nullable=False)
    
    # Usage Statistics
    usage_count = Column(Integer, default=0, nullable=False)
    last_used_at = Column(DateTime, nullable=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)  # Allow NULL for system templates
    updated_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Relationships
    company = relationship("Company", back_populates="email_templates")
    creator = relationship("User", foreign_keys=[created_by])
    updater = relationship("User", foreign_keys=[updated_by])

    def __repr__(self):
        return f"<EmailTemplate(id={self.id}, name='{self.name}', category='{self.category}', active={self.is_active})>"

class EmailPreference(Base):
    """
    User email notification preferences
    Controls what types of emails users want to receive
    """
    __tablename__ = "email_preferences"

    id = Column(Integer, primary_key=True, index=True)
    
    # User Reference
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True, index=True)
    
    # Notification Preferences
    job_application_confirmations = Column(Boolean, default=True, nullable=False)
    application_status_updates = Column(Boolean, default=True, nullable=False)
    new_job_notifications = Column(Boolean, default=False, nullable=False)
    marketing_emails = Column(Boolean, default=False, nullable=False)
    system_notifications = Column(Boolean, default=True, nullable=False)
    
    # Communication Frequency
    digest_frequency = Column(String(20), default="immediate", nullable=False)  # immediate, daily, weekly
    preferred_time = Column(String(5), nullable=True)  # HH:MM format for digest delivery
    
    # Contact Information
    backup_email = Column(String(255), nullable=True)
    sms_notifications = Column(Boolean, default=False, nullable=False)
    phone_number = Column(String(20), nullable=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    user = relationship("User", back_populates="email_preferences")

    def __repr__(self):
        return f"<EmailPreference(user_id={self.user_id}, digest_frequency='{self.digest_frequency}')>"

class EmailQueue(Base):
    """
    Email queue for batch processing and scheduling
    Manages email delivery workflow and retry logic
    """
    __tablename__ = "email_queue"

    id = Column(Integer, primary_key=True, index=True)
    
    # Queue Management
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False, index=True)
    queue_name = Column(String(50), default="default", nullable=False, index=True)
    priority_score = Column(Integer, default=100, nullable=False, index=True)
    
    # Scheduling
    execute_after = Column(DateTime, nullable=False, index=True)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Processing Status
    status = Column(String(20), default="queued", nullable=False, index=True)  # queued, processing, completed, failed
    worker_id = Column(String(100), nullable=True)
    processing_time_ms = Column(Integer, nullable=True)
    
    # Error Handling
    error_message = Column(Text, nullable=True)
    retry_after = Column(DateTime, nullable=True)
    
    # Audit fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relationships
    email = relationship("Email", backref="queue_entries")

    def __repr__(self):
        return f"<EmailQueue(id={self.id}, email_id={self.email_id}, status='{self.status}', queue='{self.queue_name}')>"