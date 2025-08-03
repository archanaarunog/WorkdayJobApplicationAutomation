"""
Pydantic schemas for Meta Portal API.
These define the data shapes for requests and responses.
"""

from pydantic import BaseModel, EmailStr
from typing import Annotated
from typing import Optional
from datetime import datetime


# User Schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: Annotated[str, 8]
    first_name: str
    last_name: str
    phone: str

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
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

# Job Schemas
class JobCreate(BaseModel):
    title: str
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
    user_id: int
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
