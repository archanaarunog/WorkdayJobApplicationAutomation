"""
Multi-tenant utility functions for Meta Portal.

This module provides helper functions for enforcing data isolation
between companies in the multi-tenant system.
"""

from sqlalchemy.orm import Session, Query
from sqlalchemy import and_
from typing import Optional, Type, TypeVar
from src.models.user import User
from src.models.job import Job
from src.models.application import Application
from src.models.company import Company

# Generic type for model classes
ModelType = TypeVar('ModelType')


def filter_by_company(
    query: Query,
    model: Type[ModelType],
    company_id: Optional[int],
    user_is_admin: bool = False
) -> Query:
    """
    Filter a SQLAlchemy query to only return records for a specific company.
    
    Args:
        query: The SQLAlchemy query object
        model: The model class being queried
        company_id: The company ID to filter by (None for super admins)
        user_is_admin: Whether the user is an admin (affects filtering rules)
    
    Returns:
        The filtered query object
    """
    
    # Super admins (no company_id) can see all data
    if company_id is None and user_is_admin:
        return query
    
    # Regular users and company admins see only their company's data
    if hasattr(model, 'company_id'):
        return query.filter(model.company_id == company_id)
    
    # If model doesn't have company_id, return as-is (shouldn't happen)
    return query


def ensure_company_access(
    db: Session,
    model: Type[ModelType],
    record_id: int,
    company_id: Optional[int],
    user_is_admin: bool = False
) -> ModelType:
    """
    Retrieve a record and ensure the user has access to it based on company context.
    
    Args:
        db: Database session
        model: The model class to query
        record_id: The ID of the record to retrieve
        company_id: The user's company ID
        user_is_admin: Whether the user is an admin
    
    Returns:
        The model instance if access is allowed
        
    Raises:
        HTTPException: If record not found or access denied
    """
    from fastapi import HTTPException, status
    
    # Get the record
    record = db.query(model).filter(model.id == record_id).first()
    
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.__name__} not found"
        )
    
    # Check company access
    if hasattr(record, 'company_id'):
        # Super admins can access all records
        if company_id is None and user_is_admin:
            return record
        
        # Company users can only access their company's records
        if record.company_id != company_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,  # Return 404 instead of 403 for security
                detail=f"{model.__name__} not found"
            )
    
    return record


def get_company_stats(db: Session, company_id: int) -> dict:
    """
    Get statistics for a specific company.
    
    Args:
        db: Database session
        company_id: The company ID
    
    Returns:
        Dictionary with company statistics
    """
    
    # Get company
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        return {}
    
    # Count records
    user_count = db.query(User).filter(User.company_id == company_id).count()
    job_count = db.query(Job).filter(Job.company_id == company_id).count()
    active_job_count = db.query(Job).filter(
        and_(Job.company_id == company_id, Job.is_active == True)
    ).count()
    application_count = db.query(Application).filter(Application.company_id == company_id).count()
    
    return {
        "company_id": company_id,
        "company_name": company.name,
        "user_count": user_count,
        "job_count": job_count,
        "active_job_count": active_job_count,
        "application_count": application_count
    }


def validate_company_admin(
    db: Session,
    user_id: int,
    company_id: int,
    action: str = "perform this action"
) -> bool:
    """
    Validate if a user is an admin for a specific company.
    
    Args:
        db: Database session
        user_id: The user ID to check
        company_id: The company ID to check admin status for
        action: Description of the action being attempted (for error messages)
    
    Returns:
        True if user is company admin
        
    Raises:
        HTTPException: If user is not authorized
    """
    from fastapi import HTTPException, status
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    # Check if user is admin and belongs to the company
    if not user.is_admin or user.company_id != company_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Admin access required for company to {action}"
        )
    
    return True


def auto_set_company_id(
    db: Session,
    record,
    company_id: Optional[int],
    source_model: Optional[Type] = None,
    source_id: Optional[int] = None
):
    """
    Automatically set company_id for a new record.
    
    Args:
        db: Database session
        record: The record object to update
        company_id: The user's company ID
        source_model: Optional source model to inherit company_id from
        source_id: Optional source record ID to inherit company_id from
    """
    
    # If company_id is already set, don't override it
    if hasattr(record, 'company_id') and getattr(record, 'company_id') is not None:
        return
    
    # If we have a source model/ID, inherit from there
    if source_model and source_id and hasattr(source_model, 'company_id'):
        source_record = db.query(source_model).filter(source_model.id == source_id).first()
        if source_record and hasattr(source_record, 'company_id'):
            setattr(record, 'company_id', source_record.company_id)
            return
    
    # Otherwise, use the user's company_id
    if hasattr(record, 'company_id') and company_id is not None:
        setattr(record, 'company_id', company_id)