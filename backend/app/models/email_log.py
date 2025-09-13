# app/models/email_log.py
from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import relationship

from app.core.database import Base


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

    # (Optional) Link to User if your project has a users table.
    # If you don't have a User model, you can remove user_id and the 'user' relationship below.
    user_id = sa.Column(
        sa.Integer,
        sa.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Email details
    to_address = sa.Column(sa.String(255), nullable=False)
    subject = sa.Column(sa.String(255), nullable=False)
    body = sa.Column(sa.Text, nullable=True)

    # Delivery status
    status = sa.Column(sa.String(50), nullable=False, default="queued")  # queued/sent/failed
    error = sa.Column(sa.Text, nullable=True)

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

    # If you have a User model with `email_logs = relationship("EmailLog", back_populates="user")`,
    # keep the line below. Otherwise, switch to `backref="email_logs"` or remove it.
    user = relationship("User", back_populates="email_logs", viewonly=False)
