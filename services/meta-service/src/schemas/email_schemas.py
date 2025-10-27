"""
Pydantic schemas for Email-related models.
These define the structure for API requests and responses.
"""

from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

# Enums for validation
class EmailStatusEnum(str, Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"

class EmailPriorityEnum(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class DigestFrequencyEnum(str, Enum):
    IMMEDIATE = "immediate"
    DAILY = "daily"
    WEEKLY = "weekly"

# ==========================================
# EMAIL SCHEMAS
# ==========================================

class EmailBase(BaseModel):
    """Base schema for Email model"""
    recipient_email: EmailStr
    recipient_name: Optional[str] = None
    subject: str = Field(..., max_length=500)
    html_content: Optional[str] = None
    text_content: Optional[str] = None
    template_name: Optional[str] = None
    template_data: Optional[Dict[str, Any]] = None
    priority: EmailPriorityEnum = EmailPriorityEnum.NORMAL
    scheduled_at: Optional[datetime] = None

class EmailCreate(EmailBase):
    """Schema for creating a new email"""
    company_id: Optional[int] = None
    user_id: Optional[int] = None
    application_id: Optional[int] = None
    job_id: Optional[int] = None
    tracking_enabled: bool = False

class EmailUpdate(BaseModel):
    """Schema for updating an email"""
    status: Optional[EmailStatusEnum] = None
    failed_reason: Optional[str] = None
    retry_count: Optional[int] = None
    sent_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    opened_at: Optional[datetime] = None

class EmailResponse(EmailBase):
    """Schema for email API responses"""
    id: int
    sender_email: str
    sender_name: Optional[str]
    status: EmailStatusEnum
    sent_at: Optional[datetime]
    delivered_at: Optional[datetime]
    opened_at: Optional[datetime]
    failed_reason: Optional[str]
    retry_count: int
    max_retries: int
    tracking_enabled: bool
    tracking_id: Optional[str]
    external_message_id: Optional[str]
    company_id: Optional[int]
    user_id: Optional[int]
    application_id: Optional[int]
    job_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ==========================================
# EMAIL TEMPLATE SCHEMAS
# ==========================================

class EmailTemplateBase(BaseModel):
    """Base schema for EmailTemplate model"""
    name: str = Field(..., max_length=100)
    display_name: str = Field(..., max_length=200)
    description: Optional[str] = None
    subject_template: str = Field(..., max_length=500)
    html_content: Optional[str] = None
    text_content: str
    variables: Optional[List[str]] = None
    category: Optional[str] = Field(None, max_length=50)
    language: str = Field(default="en", max_length=10)

class EmailTemplateCreate(EmailTemplateBase):
    """Schema for creating a new email template"""
    company_id: Optional[int] = None
    is_system_template: bool = False
    is_active: bool = True

class EmailTemplateUpdate(BaseModel):
    """Schema for updating an email template"""
    display_name: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    subject_template: Optional[str] = Field(None, max_length=500)
    html_content: Optional[str] = None
    text_content: Optional[str] = None
    variables: Optional[List[str]] = None
    category: Optional[str] = Field(None, max_length=50)
    is_active: Optional[bool] = None

class EmailTemplateResponse(EmailTemplateBase):
    """Schema for email template API responses"""
    id: int
    company_id: Optional[int]
    is_system_template: bool
    is_active: bool
    version: int
    usage_count: int
    last_used_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    created_by: int
    updated_by: Optional[int]

    class Config:
        from_attributes = True

# ==========================================
# EMAIL PREFERENCE SCHEMAS
# ==========================================

class EmailPreferenceBase(BaseModel):
    """Base schema for EmailPreference model"""
    job_application_confirmations: bool = True
    application_status_updates: bool = True
    new_job_notifications: bool = False
    marketing_emails: bool = False
    system_notifications: bool = True
    digest_frequency: DigestFrequencyEnum = DigestFrequencyEnum.IMMEDIATE
    preferred_time: Optional[str] = Field(None, pattern=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    backup_email: Optional[EmailStr] = None
    sms_notifications: bool = False
    phone_number: Optional[str] = Field(None, max_length=20)

class EmailPreferenceCreate(EmailPreferenceBase):
    """Schema for creating email preferences"""
    pass

class EmailPreferenceUpdate(BaseModel):
    """Schema for updating email preferences"""
    job_application_confirmations: Optional[bool] = None
    application_status_updates: Optional[bool] = None
    new_job_notifications: Optional[bool] = None
    marketing_emails: Optional[bool] = None
    system_notifications: Optional[bool] = None
    digest_frequency: Optional[DigestFrequencyEnum] = None
    preferred_time: Optional[str] = Field(None, pattern=r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$')
    backup_email: Optional[EmailStr] = None
    sms_notifications: Optional[bool] = None
    phone_number: Optional[str] = Field(None, max_length=20)

class EmailPreferenceResponse(EmailPreferenceBase):
    """Schema for email preference API responses"""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ==========================================
# EMAIL QUEUE SCHEMAS
# ==========================================

class EmailQueueResponse(BaseModel):
    """Schema for email queue API responses"""
    id: int
    email_id: int
    queue_name: str
    priority_score: int
    execute_after: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    status: str
    worker_id: Optional[str]
    processing_time_ms: Optional[int]
    error_message: Optional[str]
    retry_after: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# ==========================================
# UTILITY SCHEMAS
# ==========================================

class SendEmailRequest(BaseModel):
    """Schema for manual email sending requests"""
    recipient_email: EmailStr
    recipient_name: Optional[str] = None
    template_name: str
    template_data: Dict[str, Any] = {}
    priority: EmailPriorityEnum = EmailPriorityEnum.NORMAL
    scheduled_at: Optional[datetime] = None

class EmailStatsResponse(BaseModel):
    """Schema for email statistics"""
    total_emails: int
    sent_emails: int
    failed_emails: int
    pending_emails: int
    success_rate: float
    avg_processing_time_ms: Optional[float]
    emails_last_24h: int
    emails_last_7d: int
    popular_templates: List[Dict[str, Any]]

class TestEmailRequest(BaseModel):
    """Schema for test email requests"""
    recipient_email: EmailStr
    template_name: str
    template_data: Dict[str, Any] = {}

# ==========================================
# BULK OPERATION SCHEMAS
# ==========================================

class BulkEmailRequest(BaseModel):
    """Schema for bulk email operations"""
    recipients: List[EmailStr]
    template_name: str
    template_data: Dict[str, Any] = {}
    priority: EmailPriorityEnum = EmailPriorityEnum.NORMAL
    scheduled_at: Optional[datetime] = None

class BulkEmailResponse(BaseModel):
    """Schema for bulk email operation responses"""
    total_requested: int
    emails_queued: int
    failed_validations: List[Dict[str, str]]
    batch_id: str