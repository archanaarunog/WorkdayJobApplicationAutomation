"""
Email management API routes for Meta Portal.
Handles email operations, template management, and notification settings.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import logging

from ..config.database import get_db
from ..models.email import Email, EmailTemplate, EmailPreference, EmailQueue, EmailStatus, EmailPriority
from ..models.user import User
from ..models.company import Company
from ..schemas.email_schemas import (
    EmailResponse, EmailCreate, EmailUpdate,
    EmailTemplateResponse, EmailTemplateCreate, EmailTemplateUpdate,
    EmailPreferenceResponse, EmailPreferenceCreate, EmailPreferenceUpdate,
    SendEmailRequest, EmailStatsResponse, TestEmailRequest, BulkEmailRequest, BulkEmailResponse
)
from ..services.email_service import email_service
from ..utils.auth import get_current_active_user, get_current_admin_user, get_user_company
from ..utils.multitenant import get_company_stats

logger = logging.getLogger(__name__)
router = APIRouter()

# ==========================================
# EMAIL MANAGEMENT ENDPOINTS (ADMIN)
# ==========================================

@router.get("/admin/emails", response_model=List[EmailResponse])
async def get_all_emails(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    status: Optional[EmailStatus] = None,
    template_name: Optional[str] = None,
    recipient_email: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get all emails with filtering options (Admin only)"""
    try:
        company = get_user_company(db, current_user)
        query = db.query(Email)
        
        # Filter by company if user is not super admin
        if company:
            query = query.filter(Email.company_id == company.id)
        
        # Apply filters
        if status:
            query = query.filter(Email.status == status)
        if template_name:
            query = query.filter(Email.template_name == template_name)
        if recipient_email:
            query = query.filter(Email.recipient_email.ilike(f"%{recipient_email}%"))
        if date_from:
            query = query.filter(Email.created_at >= date_from)
        if date_to:
            query = query.filter(Email.created_at <= date_to)
        
        # Order by most recent first
        emails = query.order_by(Email.created_at.desc()).offset(skip).limit(limit).all()
        return emails
    
    except Exception as e:
        logger.error(f"Error fetching emails: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch emails")

@router.get("/admin/emails/{email_id}", response_model=EmailResponse)
async def get_email_by_id(
    email_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get specific email by ID (Admin only)"""
    try:
        email = db.query(Email).filter(Email.id == email_id).first()
        if not email:
            raise HTTPException(status_code=404, detail="Email not found")
        
        # Check company access
        company = get_user_company(db, current_user)
        if company and email.company_id != company.id:
            raise HTTPException(status_code=403, detail="Access denied")
        
        return email
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching email {email_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch email")

@router.post("/admin/emails/send", response_model=EmailResponse)
async def send_email_manually(
    email_request: SendEmailRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Send email manually (Admin only)"""
    try:
        company = get_user_company(db, current_user)
        company_id = company.id if company else None
        
        # Send email asynchronously
        email = await email_service.send_email_async(
            db=db,
            recipient_email=email_request.recipient_email,
            template_name=email_request.template_name,
            template_data=email_request.template_data,
            priority=email_request.priority,
            scheduled_at=email_request.scheduled_at,
            company_id=company_id
        )
        
        return email
    
    except Exception as e:
        logger.error(f"Error sending manual email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send email: {str(e)}")

@router.post("/admin/emails/bulk-send", response_model=BulkEmailResponse)
async def send_bulk_emails(
    bulk_request: BulkEmailRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Send emails to multiple recipients (Admin only)"""
    try:
        company = get_user_company(db, current_user)
        company_id = company.id if company else None
        
        emails_queued = 0
        failed_validations = []
        
        for recipient in bulk_request.recipients:
            try:
                await email_service.send_email_async(
                    db=db,
                    recipient_email=recipient,
                    template_name=bulk_request.template_name,
                    template_data=bulk_request.template_data,
                    priority=bulk_request.priority,
                    scheduled_at=bulk_request.scheduled_at,
                    company_id=company_id
                )
                emails_queued += 1
            
            except Exception as e:
                failed_validations.append({
                    "email": recipient,
                    "error": str(e)
                })
        
        return BulkEmailResponse(
            total_requested=len(bulk_request.recipients),
            emails_queued=emails_queued,
            failed_validations=failed_validations,
            batch_id=f"bulk_{datetime.utcnow().timestamp()}"
        )
    
    except Exception as e:
        logger.error(f"Error sending bulk emails: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send bulk emails: {str(e)}")

@router.post("/admin/emails/test")
async def send_test_email(
    test_request: TestEmailRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Send test email for template validation (Admin only)"""
    try:
        company = get_user_company(db, current_user)
        company_id = company.id if company else None
        
        # Add test indicator to template data
        template_data = test_request.template_data.copy()
        template_data.update({
            "is_test_email": True,
            "test_sender": current_user.first_name + " " + current_user.last_name
        })
        
        email = await email_service.send_email_async(
            db=db,
            recipient_email=test_request.recipient_email,
            template_name=test_request.template_name,
            template_data=template_data,
            priority=EmailPriority.HIGH,
            company_id=company_id
        )
        
        return {"message": "Test email sent successfully", "email_id": email.id}
    
    except Exception as e:
        logger.error(f"Error sending test email: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to send test email: {str(e)}")

@router.get("/admin/emails/stats", response_model=EmailStatsResponse)
async def get_email_statistics(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get email statistics (Admin only)"""
    try:
        company = get_user_company(db, current_user)
        company_id = company.id if company else None
        
        stats = email_service.get_email_stats(db, company_id)
        
        # Add popular templates
        query = db.query(EmailTemplate.name, EmailTemplate.usage_count)
        if company_id:
            query = query.filter(EmailTemplate.company_id == company_id)
        
        popular_templates = query.order_by(EmailTemplate.usage_count.desc()).limit(5).all()
        stats["popular_templates"] = [
            {"name": name, "usage_count": count} 
            for name, count in popular_templates
        ]
        
        return stats
    
    except Exception as e:
        logger.error(f"Error fetching email stats: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch email statistics")

# ==========================================
# EMAIL TEMPLATE MANAGEMENT ENDPOINTS
# ==========================================

@router.get("/admin/email-templates", response_model=List[EmailTemplateResponse])
async def get_email_templates(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=200),
    category: Optional[str] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get all email templates (Admin only)"""
    try:
        company = get_user_company(db, current_user)
        query = db.query(EmailTemplate)
        
        # Show system templates and company-specific templates
        if company:
            query = query.filter(
                (EmailTemplate.company_id == company.id) | 
                (EmailTemplate.is_system_template == True)
            )
        
        # Apply filters
        if category:
            query = query.filter(EmailTemplate.category == category)
        if is_active is not None:
            query = query.filter(EmailTemplate.is_active == is_active)
        
        templates = query.order_by(EmailTemplate.name).offset(skip).limit(limit).all()
        return templates
    
    except Exception as e:
        logger.error(f"Error fetching email templates: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch email templates")

@router.post("/admin/email-templates", response_model=EmailTemplateResponse)
async def create_email_template(
    template: EmailTemplateCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Create new email template (Admin only)"""
    try:
        # Check if template name already exists
        existing = db.query(EmailTemplate).filter(EmailTemplate.name == template.name).first()
        if existing:
            raise HTTPException(status_code=400, detail="Template with this name already exists")
        
        company = get_user_company(db, current_user)
        
        db_template = EmailTemplate(
            **template.dict(),
            company_id=company.id if company else None,
            created_by=current_user.id
        )
        
        db.add(db_template)
        db.commit()
        db.refresh(db_template)
        
        logger.info(f"Email template '{template.name}' created by user {current_user.id}")
        return db_template
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating email template: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create email template")

@router.put("/admin/email-templates/{template_id}", response_model=EmailTemplateResponse)
async def update_email_template(
    template_id: int,
    template_update: EmailTemplateUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Update email template (Admin only)"""
    try:
        template = db.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Check access permissions
        company = get_user_company(db, current_user)
        if template.company_id and (not company or template.company_id != company.id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Update template
        update_data = template_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(template, field, value)
        
        template.updated_by = current_user.id
        template.version += 1
        
        db.commit()
        db.refresh(template)
        
        logger.info(f"Email template {template_id} updated by user {current_user.id}")
        return template
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating email template {template_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update email template")

@router.delete("/admin/email-templates/{template_id}")
async def delete_email_template(
    template_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Delete email template (Admin only)"""
    try:
        template = db.query(EmailTemplate).filter(EmailTemplate.id == template_id).first()
        if not template:
            raise HTTPException(status_code=404, detail="Template not found")
        
        # Check access permissions
        company = get_user_company(db, current_user)
        if template.company_id and (not company or template.company_id != company.id):
            raise HTTPException(status_code=403, detail="Access denied")
        
        # Prevent deletion of system templates
        if template.is_system_template:
            raise HTTPException(status_code=400, detail="Cannot delete system templates")
        
        # Check if template is in use
        emails_using_template = db.query(Email).filter(
            Email.template_name == template.name,
            Email.status.in_([EmailStatus.PENDING, EmailStatus.RETRYING])
        ).count()
        
        if emails_using_template > 0:
            raise HTTPException(
                status_code=400, 
                detail=f"Cannot delete template. {emails_using_template} emails are using this template."
            )
        
        db.delete(template)
        db.commit()
        
        logger.info(f"Email template {template_id} deleted by user {current_user.id}")
        return {"message": "Template deleted successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting email template {template_id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to delete email template")

# ==========================================
# USER EMAIL PREFERENCES ENDPOINTS
# ==========================================

@router.get("/user/email-preferences", response_model=EmailPreferenceResponse)
async def get_user_email_preferences(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get current user's email preferences"""
    try:
        preferences = db.query(EmailPreference).filter(
            EmailPreference.user_id == current_user.id
        ).first()
        
        if not preferences:
            # Create default preferences
            preferences = EmailPreference(user_id=current_user.id)
            db.add(preferences)
            db.commit()
            db.refresh(preferences)
        
        return preferences
    
    except Exception as e:
        logger.error(f"Error fetching email preferences for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch email preferences")

@router.put("/user/email-preferences", response_model=EmailPreferenceResponse)
async def update_user_email_preferences(
    preferences_update: EmailPreferenceUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update current user's email preferences"""
    try:
        preferences = db.query(EmailPreference).filter(
            EmailPreference.user_id == current_user.id
        ).first()
        
        if not preferences:
            # Create new preferences with updates
            preferences = EmailPreference(
                user_id=current_user.id,
                **preferences_update.dict(exclude_unset=True)
            )
            db.add(preferences)
        else:
            # Update existing preferences
            update_data = preferences_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(preferences, field, value)
        
        db.commit()
        db.refresh(preferences)
        
        logger.info(f"Email preferences updated for user {current_user.id}")
        return preferences
    
    except Exception as e:
        logger.error(f"Error updating email preferences for user {current_user.id}: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to update email preferences")

# ==========================================
# EMAIL QUEUE MONITORING (ADMIN)
# ==========================================

@router.get("/admin/email-queue")
async def get_email_queue_status(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, le=200),
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Get email queue status (Admin only)"""
    try:
        query = db.query(EmailQueue)
        
        if status:
            query = query.filter(EmailQueue.status == status)
        
        queue_entries = query.order_by(
            EmailQueue.priority_score.desc(), 
            EmailQueue.execute_after
        ).offset(skip).limit(limit).all()
        
        return queue_entries
    
    except Exception as e:
        logger.error(f"Error fetching email queue: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch email queue")

@router.post("/admin/email-queue/process")
async def process_email_queue_manually(
    background_tasks: BackgroundTasks,
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user)
):
    """Manually trigger email queue processing (Admin only)"""
    try:
        # Add background task to process queue
        background_tasks.add_task(email_service.process_email_queue, db, limit)
        
        return {"message": f"Email queue processing started (limit: {limit})"}
    
    except Exception as e:
        logger.error(f"Error triggering email queue processing: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process email queue")