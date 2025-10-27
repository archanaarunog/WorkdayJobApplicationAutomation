"""
Authentication utilities for Meta Portal.
Provides authentication dependencies for FastAPI routes.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from ..config.database import get_db
from ..models.user import User

# OAuth2 scheme for extracting token from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/login")

# IMPORTANT: Use the same secret key and algorithm as your auth service
SECRET_KEY = "DittoDolly@0806"  # Must match src/services/auth.py
ALGORITHM = "HS256"

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """Get current user from JWT token"""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        company_id: int = payload.get("company_id")
        user_id: int = payload.get("user_id")
        
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Query user by email and validate company_id matches
    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception
    
    # Additional security: verify token's company_id matches user's actual company_id
    # This prevents token reuse across different companies
    if company_id is not None and user.company_id != company_id:
        raise HTTPException(
            status_code=401,
            detail="Invalid company context",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user (must be active)"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=400, 
            detail="Inactive user"
        )
    return current_user

def get_current_admin_user(current_user: User = Depends(get_current_active_user)) -> User:
    """Get current admin user (must be active and admin)"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions. Admin access required."
        )
    return current_user

def get_user_company_context(token: str = Depends(oauth2_scheme)) -> dict:
    """Extract company context from JWT token without database query."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "user_id": payload.get("user_id"),
            "company_id": payload.get("company_id"),
            "email": payload.get("sub"),
            "is_admin": payload.get("is_admin", False)
        }
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_user_company(db: Session, user: User):
    """Get the company associated with the user"""
    from ..models.company import Company
    if user.company_id:
        return db.query(Company).filter(Company.id == user.company_id).first()
    return None