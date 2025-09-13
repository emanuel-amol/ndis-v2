# app/models/referral.py
from __future__ import annotations

import uuid
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship

from app.core.database import Base


class Referral(Base):
    __tablename__ = "referrals"

    # Primary key (UUID)
    id = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Client Details
    first_name = sa.Column(sa.String(100), nullable=False)
    last_name = sa.Column(sa.String(100), nullable=False)
    date_of_birth = sa.Column(sa.Date, nullable=False)
    phone_number = sa.Column(sa.String(40), nullable=False)
    email_address = sa.Column(sa.String(255), nullable=True)
    street_address = sa.Column(sa.String(255), nullable=False)
    city = sa.Column(sa.String(100), nullable=False)
    state = sa.Column(sa.String(100), nullable=False)
    postcode = sa.Column(sa.String(20), nullable=False)
    preferred_contact = sa.Column(sa.String(50), nullable=False, default="phone")

    # Representative Details (Optional)
    rep_first_name = sa.Column(sa.String(100), nullable=True)
    rep_last_name = sa.Column(sa.String(100), nullable=True)
    rep_phone_number = sa.Column(sa.String(40), nullable=True)
    rep_email_address = sa.Column(sa.String(255), nullable=True)
    rep_street_address = sa.Column(sa.String(255), nullable=True)
    rep_city = sa.Column(sa.String(100), nullable=True)
    rep_state = sa.Column(sa.String(100), nullable=True)
    rep_postcode = sa.Column(sa.String(20), nullable=True)
    rep_relationship = sa.Column(sa.String(100), nullable=True)

    # NDIS Details
    plan_type = sa.Column(sa.String(50), nullable=False)
    plan_manager_name = sa.Column(sa.String(100), nullable=True)
    plan_manager_agency = sa.Column(sa.String(100), nullable=True)
    ndis_number = sa.Column(sa.String(50), nullable=True)
    available_funding = sa.Column(sa.String(100), nullable=True)
    plan_start_date = sa.Column(sa.Date, nullable=False)
    plan_review_date = sa.Column(sa.Date, nullable=False)
    client_goals = sa.Column(sa.Text, nullable=False)

    # Referrer Details
    referrer_first_name = sa.Column(sa.String(100), nullable=False)
    referrer_last_name = sa.Column(sa.String(100), nullable=False)
    referrer_agency = sa.Column(sa.String(100), nullable=True)
    referrer_role = sa.Column(sa.String(100), nullable=True)
    referrer_email = sa.Column(sa.String(255), nullable=False)
    referrer_phone = sa.Column(sa.String(40), nullable=False)

    # Reason for Referral
    referred_for = sa.Column(sa.String(50), nullable=False)
    reason_for_referral = sa.Column(sa.Text, nullable=False)

    # Consent
    consent_checkbox = sa.Column(sa.Boolean, nullable=False, default=False)

    # Status + metadata
    status = sa.Column(sa.String(32), nullable=False, default="new")
    notes = sa.Column(sa.Text, nullable=True)

    # Audit fields
    raw_submission = sa.Column(sa.JSON, nullable=True)
    form_metadata = sa.Column(sa.JSON, nullable=True)

    # Legacy NDIS fields (for backward compatibility)
    disability_type = sa.Column(sa.String(100), nullable=True)
    service_types = sa.Column(ARRAY(sa.String), nullable=True)
    urgency_level = sa.Column(sa.String(20), nullable=True)
    preferred_contact_method = sa.Column(sa.String(50), nullable=True)
    current_supports = sa.Column(sa.Text, nullable=True)
    support_goals = sa.Column(sa.Text, nullable=True)
    accessibility_needs = sa.Column(sa.Text, nullable=True)
    cultural_considerations = sa.Column(sa.Text, nullable=True)

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
    email_logs = relationship(
        "EmailLog",
        back_populates="referral",
        cascade="all, delete-orphan",
    )