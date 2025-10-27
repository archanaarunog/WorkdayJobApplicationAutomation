"""
Email Service Layer for Meta Portal.
Handles SMTP integration, template rendering, and email sending operations.
"""

import smtplib
import asyncio
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, Any, Optional, List
import logging
from datetime import datetime, timedelta
import uuid
import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template
from sqlalchemy.orm import Session

from ..config.database import get_db
from ..models.email import Email, EmailTemplate, EmailQueue, EmailStatus, EmailPriority
from ..models.user import User
from ..models.company import Company

# Configure logging
logger = logging.getLogger(__name__)

class EmailConfig:
    """Email configuration settings"""
    
    # SMTP Settings - Can be overridden by environment variables
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    USE_TLS = os.getenv("USE_TLS", "true").lower() == "true"
    
    # Default sender settings
    DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "noreply@metaportal.com")
    DEFAULT_FROM_NAME = os.getenv("DEFAULT_FROM_NAME", "Meta Portal")
    
    # Admin settings
    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@metaportal.com")
    
    # Template settings
    TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "templates", "email")
    
    # Email limits and retry settings
    MAX_RETRIES = int(os.getenv("EMAIL_MAX_RETRIES", "3"))
    RETRY_DELAY_MINUTES = int(os.getenv("EMAIL_RETRY_DELAY", "30"))
    RATE_LIMIT_PER_MINUTE = int(os.getenv("EMAIL_RATE_LIMIT", "60"))

class EmailTemplateEngine:
    """Template engine for rendering email content"""
    
    def __init__(self):
        # Create templates directory if it doesn't exist
        os.makedirs(EmailConfig.TEMPLATE_DIR, exist_ok=True)
        
        # Initialize Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(EmailConfig.TEMPLATE_DIR),
            autoescape=True
        )
    
    def render_template(self, template_name: str, variables: Dict[str, Any]) -> tuple[str, str]:
        """
        Render email template with provided variables
        Returns: (html_content, text_content)
        """
        try:
            # Load HTML template
            html_template = self.env.get_template(f"{template_name}.html")
            html_content = html_template.render(**variables)
            
            # Try to load text template, fallback to HTML if not found
            try:
                text_template = self.env.get_template(f"{template_name}.txt")
                text_content = text_template.render(**variables)
            except:
                # Simple HTML to text conversion as fallback
                text_content = self._html_to_text(html_content)
            
            return html_content, text_content
        
        except Exception as e:
            logger.error(f"Error rendering template {template_name}: {str(e)}")
            raise Exception(f"Template rendering failed: {str(e)}")
    
    def render_template_from_db(self, template: EmailTemplate, variables: Dict[str, Any]) -> tuple[str, str, str]:
        """
        Render email template from database template
        Returns: (subject, html_content, text_content)
        """
        try:
            # Render subject
            subject_template = Template(template.subject_template)
            subject = subject_template.render(**variables)
            
            # Render HTML content
            html_content = None
            if template.html_content:
                html_template = Template(template.html_content)
                html_content = html_template.render(**variables)
            
            # Render text content
            text_template = Template(template.text_content)
            text_content = text_template.render(**variables)
            
            return subject, html_content, text_content
        
        except Exception as e:
            logger.error(f"Error rendering database template {template.name}: {str(e)}")
            raise Exception(f"Database template rendering failed: {str(e)}")
    
    def _html_to_text(self, html_content: str) -> str:
        """Simple HTML to text conversion"""
        import re
        # Remove HTML tags
        text = re.sub('<[^<]+?>', '', html_content)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text

class SMTPEmailSender:
    """SMTP email sending service"""
    
    def __init__(self):
        self.config = EmailConfig()
    
    def send_email(self, email_data: Dict[str, Any]) -> bool:
        """
        Send email via SMTP
        Returns: True if successful, False otherwise
        """
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{email_data.get('sender_name', self.config.DEFAULT_FROM_NAME)} <{email_data.get('sender_email', self.config.DEFAULT_FROM_EMAIL)}>"
            msg['To'] = email_data['recipient_email']
            msg['Subject'] = email_data['subject']
            
            # Add tracking ID to headers if enabled
            if email_data.get('tracking_id'):
                msg['X-Tracking-ID'] = email_data['tracking_id']
            
            # Add text content
            if email_data.get('text_content'):
                text_part = MIMEText(email_data['text_content'], 'plain')
                msg.attach(text_part)
            
            # Add HTML content
            if email_data.get('html_content'):
                html_part = MIMEText(email_data['html_content'], 'html')
                msg.attach(html_part)
            
            # Connect to SMTP server and send
            with smtplib.SMTP(self.config.SMTP_SERVER, self.config.SMTP_PORT) as server:
                if self.config.USE_TLS:
                    server.starttls()
                
                if self.config.SMTP_USERNAME and self.config.SMTP_PASSWORD:
                    server.login(self.config.SMTP_USERNAME, self.config.SMTP_PASSWORD)
                
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {email_data['recipient_email']}")
            return True
        
        except Exception as e:
            logger.error(f"Failed to send email to {email_data['recipient_email']}: {str(e)}")
            return False

class EmailService:
    """Main email service class"""
    
    def __init__(self):
        self.template_engine = EmailTemplateEngine()
        self.smtp_sender = SMTPEmailSender()
    
    async def send_email_async(
        self,
        db: Session,
        recipient_email: str,
        template_name: str,
        template_data: Dict[str, Any] = None,
        sender_email: str = None,
        sender_name: str = None,
        priority: EmailPriority = EmailPriority.NORMAL,
        scheduled_at: datetime = None,
        company_id: int = None,
        user_id: int = None,
        application_id: int = None,
        job_id: int = None,
        tracking_enabled: bool = False
    ) -> Email:
        """
        Async email sending with database tracking
        """
        if template_data is None:
            template_data = {}
        
        try:
            # Get template from database
            template = db.query(EmailTemplate).filter(
                EmailTemplate.name == template_name,
                EmailTemplate.is_active == True
            ).first()
            
            if not template:
                raise Exception(f"Template '{template_name}' not found or inactive")
            
            # Render template
            subject, html_content, text_content = self.template_engine.render_template_from_db(
                template, template_data
            )
            
            # Generate tracking ID if enabled
            tracking_id = str(uuid.uuid4()) if tracking_enabled else None
            
            # Create email record in database
            email = Email(
                recipient_email=recipient_email,
                recipient_name=template_data.get('recipient_name'),
                sender_email=sender_email or EmailConfig.DEFAULT_FROM_EMAIL,
                sender_name=sender_name or EmailConfig.DEFAULT_FROM_NAME,
                subject=subject,
                html_content=html_content,
                text_content=text_content,
                template_name=template_name,
                template_data=template_data,
                priority=priority,
                scheduled_at=scheduled_at or datetime.utcnow(),
                company_id=company_id,
                user_id=user_id,
                application_id=application_id,
                job_id=job_id,
                tracking_enabled=tracking_enabled,
                tracking_id=tracking_id,
                status=EmailStatus.PENDING
            )
            
            db.add(email)
            db.commit()
            db.refresh(email)
            
            # Add to queue if scheduled for later, otherwise send immediately
            if scheduled_at and scheduled_at > datetime.utcnow():
                await self._add_to_queue(db, email)
            else:
                await self._send_email_now(db, email)
            
            return email
        
        except Exception as e:
            logger.error(f"Error in send_email_async: {str(e)}")
            db.rollback()
            raise
    
    async def _send_email_now(self, db: Session, email: Email):
        """Send email immediately"""
        try:
            email.status = EmailStatus.PENDING
            db.commit()
            
            # Prepare email data for SMTP sender
            email_data = {
                'recipient_email': email.recipient_email,
                'sender_email': email.sender_email,
                'sender_name': email.sender_name,
                'subject': email.subject,
                'html_content': email.html_content,
                'text_content': email.text_content,
                'tracking_id': email.tracking_id
            }
            
            # Send via SMTP
            success = self.smtp_sender.send_email(email_data)
            
            if success:
                email.status = EmailStatus.SENT
                email.sent_at = datetime.utcnow()
            else:
                email.status = EmailStatus.FAILED
                email.failed_reason = "SMTP sending failed"
                email.retry_count += 1
                
                # Schedule retry if under max retries
                if email.retry_count < email.max_retries:
                    await self._schedule_retry(db, email)
            
            db.commit()
        
        except Exception as e:
            logger.error(f"Error sending email {email.id}: {str(e)}")
            email.status = EmailStatus.FAILED
            email.failed_reason = str(e)
            email.retry_count += 1
            db.commit()
    
    async def _add_to_queue(self, db: Session, email: Email):
        """Add email to processing queue"""
        try:
            queue_entry = EmailQueue(
                email_id=email.id,
                queue_name="default",
                priority_score=self._get_priority_score(email.priority),
                execute_after=email.scheduled_at,
                status="queued"
            )
            
            db.add(queue_entry)
            db.commit()
            
            logger.info(f"Email {email.id} added to queue for execution at {email.scheduled_at}")
        
        except Exception as e:
            logger.error(f"Error adding email {email.id} to queue: {str(e)}")
            raise
    
    async def _schedule_retry(self, db: Session, email: Email):
        """Schedule email for retry"""
        retry_time = datetime.utcnow() + timedelta(minutes=EmailConfig.RETRY_DELAY_MINUTES)
        
        queue_entry = EmailQueue(
            email_id=email.id,
            queue_name="retry",
            priority_score=self._get_priority_score(email.priority) + 50,  # Higher priority for retries
            execute_after=retry_time,
            status="queued"
        )
        
        db.add(queue_entry)
        db.commit()
        
        logger.info(f"Email {email.id} scheduled for retry at {retry_time}")
    
    def _get_priority_score(self, priority: EmailPriority) -> int:
        """Convert priority to numeric score for queue processing"""
        priority_scores = {
            EmailPriority.LOW: 25,
            EmailPriority.NORMAL: 100,
            EmailPriority.HIGH: 200,
            EmailPriority.URGENT: 500
        }
        return priority_scores.get(priority, 100)
    
    async def process_email_queue(self, db: Session, limit: int = 50):
        """Process queued emails"""
        try:
            # Get queued emails ready for processing
            queue_entries = db.query(EmailQueue).filter(
                EmailQueue.status == "queued",
                EmailQueue.execute_after <= datetime.utcnow()
            ).order_by(
                EmailQueue.priority_score.desc(),
                EmailQueue.execute_after
            ).limit(limit).all()
            
            for queue_entry in queue_entries:
                try:
                    queue_entry.status = "processing"
                    queue_entry.started_at = datetime.utcnow()
                    db.commit()
                    
                    # Send the email
                    await self._send_email_now(db, queue_entry.email)
                    
                    queue_entry.status = "completed"
                    queue_entry.completed_at = datetime.utcnow()
                    db.commit()
                
                except Exception as e:
                    logger.error(f"Error processing queue entry {queue_entry.id}: {str(e)}")
                    queue_entry.status = "failed"
                    queue_entry.error_message = str(e)
                    db.commit()
        
        except Exception as e:
            logger.error(f"Error processing email queue: {str(e)}")
    
    def get_email_stats(self, db: Session, company_id: Optional[int] = None) -> Dict[str, Any]:
        """Get email statistics"""
        query = db.query(Email)
        if company_id:
            query = query.filter(Email.company_id == company_id)
        
        total_emails = query.count()
        sent_emails = query.filter(Email.status == EmailStatus.SENT).count()
        failed_emails = query.filter(Email.status == EmailStatus.FAILED).count()
        pending_emails = query.filter(Email.status == EmailStatus.PENDING).count()
        
        success_rate = (sent_emails / total_emails * 100) if total_emails > 0 else 0
        
        # Recent activity
        last_24h = query.filter(Email.created_at >= datetime.utcnow() - timedelta(hours=24)).count()
        last_7d = query.filter(Email.created_at >= datetime.utcnow() - timedelta(days=7)).count()
        
        return {
            "total_emails": total_emails,
            "sent_emails": sent_emails,
            "failed_emails": failed_emails,
            "pending_emails": pending_emails,
            "success_rate": round(success_rate, 2),
            "emails_last_24h": last_24h,
            "emails_last_7d": last_7d
        }

# Global email service instance
email_service = EmailService()