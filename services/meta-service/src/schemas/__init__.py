# This file makes the schemas directory a Python package
from .base_schemas import (
    UserCreate, UserLogin, UserRead, UserUpdate,
    JobCreate, JobRead,
    ApplicationCreate, ApplicationRead
)
from .email_schemas import (
    EmailResponse, EmailCreate, EmailUpdate,
    EmailTemplateResponse, EmailTemplateCreate, EmailTemplateUpdate,
    EmailPreferenceResponse, EmailPreferenceCreate, EmailPreferenceUpdate,
    SendEmailRequest, EmailStatsResponse, TestEmailRequest, 
    BulkEmailRequest, BulkEmailResponse
)

__all__ = [
    # Base schemas
    "UserCreate", "UserLogin", "UserRead", "UserUpdate",
    "JobCreate", "JobRead",
    "ApplicationCreate", "ApplicationRead",
    # Email schemas
    "EmailResponse", "EmailCreate", "EmailUpdate",
    "EmailTemplateResponse", "EmailTemplateCreate", "EmailTemplateUpdate",
    "EmailPreferenceResponse", "EmailPreferenceCreate", "EmailPreferenceUpdate",
    "SendEmailRequest", "EmailStatsResponse", "TestEmailRequest", 
    "BulkEmailRequest", "BulkEmailResponse"
]