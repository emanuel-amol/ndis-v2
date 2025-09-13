from __future__ import annotations

import logging
from datetime import datetime
from typing import List  # <-- needed for annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.core.database import get_db
from app.schemas.referral import ReferralCreate, ReferralResponse, ReferralUpdate
from app.services.referral_service import ReferralService
from app.services.email_service import EmailService
from app.models.user import User, UserRole, get_providers_for_service, get_admins
from app.models.referral import Referral  # <-- import the ORM model

router = APIRouter()
log = logging.getLogger(__name__)  # <-- used by .exception() calls


def orm_to_response(r: Referral) -> ReferralResponse:
    """Map ORM -> Pydantic (Pydantic v2)."""
    return ReferralResponse.model_validate(r, from_attributes=True)


def get_provider_emails_for_referral(referral, db: Session) -> List[str]:
    """
    Get provider emails based on referral type from database
    """
    provider_emails: List[str] = []
    try:
        admins = get_admins(db)
        admin_emails = [admin.email for admin in admins if admin.email]
        provider_emails.extend(admin_emails)

        service_type = (
            referral.referred_for.lower()
            if hasattr(referral, "referred_for") and referral.referred_for
            else "general"
        )
        providers = get_providers_for_service(db, service_type)
        provider_specific_emails = [p.email for p in providers if p.email]
        provider_emails.extend(provider_specific_emails)

        if not providers:
            all_providers = (
                db.query(User)
                .filter(
                    User.role == UserRole.PROVIDER,
                    User.is_active == True,  # noqa: E712
                    User.email.isnot(None),
                )
                .all()
            )
            provider_emails.extend([p.email for p in all_providers if p.email])

        return list(set(provider_emails))  # de-dup
    except Exception:
        # Fallback address if DB lookup fails
        return ["vanshikasmriti024@gmail.com"]


@router.post("/referral", response_model=ReferralResponse, status_code=status.HTTP_201_CREATED)
async def submit_referral(referral_data: ReferralCreate, db: Session = Depends(get_db)):
    """
    Public endpoint: submit a new referral form
    """
    try:
        referral = ReferralService.create_referral(db, referral_data)

        try:
            provider_emails = get_provider_emails_for_referral(referral, db)
            email_service = EmailService()
            if email_service.is_configured():
                await email_service.send_participant_confirmation(referral)
                await email_service.send_provider_notification(referral, provider_emails)
        except Exception:
            # Log but do not fail the submission
            log.exception("Failed to send email notifications for referral %s", getattr(referral, "id", "?"))

        return orm_to_response(referral)
    except Exception as e:
        log.exception("Error creating referral")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating referral: {e}",
        )


@router.get(
    "/referrals",
    response_model=list[ReferralResponse],
    name="get_referrals",
    operation_id="get_referrals",
)
def get_referrals(db: Session = Depends(get_db)) -> list[ReferralResponse]:
    rows = db.query(Referral).order_by(Referral.created_at.desc()).all()
    return [orm_to_response(r) for r in rows]


@router.get(
    "/referrals/{referral_id}",
    response_model=ReferralResponse,
    name="get_referral",
    operation_id="get_referral",
)
def get_referral(referral_id: str, db: Session = Depends(get_db)) -> ReferralResponse:
    r = db.get(Referral, referral_id)
    if not r:
        raise HTTPException(status_code=404, detail="Referral not found")
    return orm_to_response(r)


@router.put(
    "/referrals/{referral_id}",
    response_model=ReferralResponse,
    name="update_referral",
    operation_id="update_referral",
)
def update_referral(referral_id: str, body: ReferralUpdate, db: Session = Depends(get_db)) -> ReferralResponse:
    try:
        r = db.get(Referral, referral_id)
        if not r:
            raise HTTPException(status_code=404, detail="Referral not found")

        # Update only provided fields
        for api_key, value in body.model_dump(exclude_unset=True).items():
            if api_key == "firstName":                  r.first_name = value
            elif api_key == "lastName":                 r.last_name = value
            elif api_key == "dateOfBirth":              r.date_of_birth = value
            elif api_key == "phoneNumber":              r.phone_number = value
            elif api_key == "emailAddress":             r.email_address = value
            elif api_key == "streetAddress":            r.street_address = value
            elif api_key == "city":                     r.city = value
            elif api_key == "state":                    r.state = value
            elif api_key == "postcode":                 r.postcode = value
            elif api_key == "disabilityType":           r.disability_type = value
            elif api_key == "serviceTypes":             r.service_types = value
            elif api_key == "ndisNumber":               r.ndis_number = value
            elif api_key == "urgencyLevel":             r.urgency_level = value
            elif api_key == "preferredContactMethod":   r.preferred_contact_method = value
            elif api_key == "currentSupports":          r.current_supports = value
            elif api_key == "supportGoals":             r.support_goals = value
            elif api_key == "accessibilityNeeds":       r.accessibility_needs = value
            elif api_key == "culturalConsiderations":   r.cultural_considerations = value
            elif api_key == "repFirstName":             r.rep_first_name = value
            elif api_key == "repLastName":              r.rep_last_name = value
            elif api_key == "repPhoneNumber":           r.rep_phone_number = value
            elif api_key == "repEmailAddress":          r.rep_email_address = value
            elif api_key == "repRelationship":          r.rep_relationship = value

        r.updated_at = datetime.utcnow()
        db.add(r)
        db.commit()
        db.refresh(r)
        return orm_to_response(r)
    except Exception as e:
        db.rollback()
        log.exception("Update referral failed")
        raise HTTPException(status_code=500, detail=f"Referral update failed: {e!s}")


@router.delete(
    "/referrals/{referral_id}",
    name="delete_referral",
    operation_id="delete_referral",
)
def delete_referral(referral_id: str, db: Session = Depends(get_db)) -> dict:
    try:
        r = db.get(Referral, referral_id)
        if not r:
            raise HTTPException(status_code=404, detail="Referral not found")
        db.delete(r)
        db.commit()
        return {"ok": True, "deleted": referral_id}
    except Exception as e:
        db.rollback()
        log.exception("Delete referral failed")
        raise HTTPException(status_code=500, detail=f"Referral delete failed: {e!s}")
