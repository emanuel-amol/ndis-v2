# app/models/email_log.py
from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship
from enum import Enum

from app.core.database import Base


class EmailType(str, Enum):
    """Email notification types"""
    PROVIDER_NOTIFICATION = "provider_notification"
    PARTICIPANT_CONFIRMATION = "participant_confirmation"
    REFERRER_NOTIFICATION = "referrer_notification"


class EmailLog(Base):
    __tablename__ = "email_logs"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    # Link to Referral (UUID FK to referrals.id)
    referral_id = sa.Column(
        PGUUID(as_uuid=True),
        sa.ForeignKey("referrals.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # Link to User (optional)
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Email details
    email_type = sa.Column(sa.String(50), nullable=False)
    recipient_email = sa.Column(sa.String(255), nullable=False)
    subject = sa.Column(sa.String(255), nullable=False)
    body = sa.Column(sa.Text, nullable=True)

    # Delivery status
    status = sa.Column(sa.String(50), nullable=False, default="pending")  # pending/sent/failed
    error_message = sa.Column(sa.Text, nullable=True)
    retry_count = sa.Column(sa.Integer, default=0, nullable=False)
    sent_at = sa.Column(sa.DateTime(timezone=True), nullable=True)

    created_at = sa.Column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        nullable=False,
    )
    updated_at = sa.Column(
        sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False,
    )

    # Relationships
    referral = relationship("Referral", back_populates="email_logs")
    user = relationship("User", back_populates="email_logs")


def log_email_attempt(
    db, email_type: str, recipient_email: str, subject: str, referral_id=None, user_id=None
) -> EmailLog:
    """Helper function to log email attempts"""
    email_log = EmailLog(
        referral_id=referral_id,
        user_id=user_id,
        email_type=email_type,
        recipient_email=recipient_email,
        subject=subject,
        status="pending"
    )
    db.add(email_log)
    db.commit()
    db.refresh(email_log)
    return email_log


def update_email_status(db, email_log_id: int, status: str, error_message: str = None):
    """Helper function to update email status"""
    email_log = db.get(EmailLog, email_log_id)
    if email_log:
        email_log.status = status
        if error_message:
            email_log.error_message = error_message
        if status == "sent":
            email_log.sent_at = sa.func.now()
        elif status == "failed":
            email_log.retry_count += 1
        db.commit()


def get_email_stats_for_referral(db, referral_id) -> dict:
    """Get email statistics for a referral"""
    logs = db.query(EmailLog).filter(EmailLog.referral_id == referral_id).all()
    
    stats = {
        "total": len(logs),
        "sent": len([log for log in logs if log.status == "sent"]),
        "failed": len([log for log in logs if log.status == "failed"]),
        "pending": len([log for log in logs if log.status == "pending"]),
    }
    
    return stats