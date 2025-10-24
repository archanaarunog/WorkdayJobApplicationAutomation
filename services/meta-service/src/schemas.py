"""
Pydantic schemas for Meta Portal API.
These define the data shapes for requests and responses.
"""

from pydantic import BaseModel, EmailStr, validator, constr
from typing import Annotated
from typing import Optional
from datetime import datetime


# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('password must be at least 8 characters long')
        if len(v.encode('utf-8')) > 72:
            raise ValueError('password must be less than 72 bytes when encoded')
        return v

# For login (email and password only)
class UserLogin(BaseModel):
    email: EmailStr
    password: Annotated[str, 8]

class UserRead(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    bio: Optional[str]
    skills: Optional[str]
    experience: Optional[str]
    education: Optional[str]
    linkedin_url: Optional[str]
    github_url: Optional[str]
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    bio: Optional[str] = None
    skills: Optional[str] = None
    experience: Optional[str] = None
    education: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None

# Job Schemas
class JobCreate(BaseModel):
    title: str
    company: Optional[str]
    department: Optional[str]
    location: str
    job_type: Optional[str] = "Full-time"
    experience_level: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    description: str
    requirements: Optional[str]

class JobRead(BaseModel):
    id: int
    title: str
    company: Optional[str]
    department: Optional[str]
    location: str
    job_type: str
    experience_level: Optional[str]
    salary_min: Optional[int]
    salary_max: Optional[int]
    description: str
    requirements: Optional[str]
    posted_date: datetime
    is_active: bool

    class Config:
        from_attributes = True

# Application Schemas
class ApplicationCreate(BaseModel):
    job_id: int
    cover_letter: str
    additional_info: Optional[str]

class ApplicationRead(BaseModel):
    id: int
    user_id: int
    job_id: int
    cover_letter: str
    additional_info: Optional[str]
    status: str
    applied_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
