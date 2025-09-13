# backend/app/schemas/referral.py
from __future__ import annotations

from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ----------------------------
# Base models / shared fields
# ----------------------------
class ReferralBase(BaseModel):
    # Client Details
    firstName: str
    lastName: str
    dateOfBirth: date
    phoneNumber: str
    emailAddress: Optional[EmailStr] = None
    streetAddress: str
    city: str
    state: str
    postcode: str


# ----------------------------
# Create / Update payloads
# ----------------------------
class ReferralCreate(BaseModel):
    # Client Details
    firstName: str = Field(..., min_length=1, max_length=100, description="Client's first name")
    lastName: str = Field(..., min_length=1, max_length=100, description="Client's last name")
    dateOfBirth: date = Field(..., description="Client's date of birth (YYYY-MM-DD)")
    phoneNumber: str = Field(..., min_length=1, max_length=20, description="Client's phone number")
    emailAddress: Optional[EmailStr] = Field(None, description="Client's email address")
    streetAddress: str = Field(..., min_length=1, description="Client's street address")
    city: str = Field(..., min_length=1, max_length=100, description="Client's city")
    state: str = Field(..., min_length=1, max_length=10, description="Client's state")
    postcode: str = Field(..., min_length=1, max_length=10, description="Client's postcode")
    preferredContact: str = Field(..., min_length=1, max_length=20, description="Preferred contact method")

    # Representative Details (Optional)
    repFirstName: Optional[str] = Field(None, max_length=100, description="Representative's first name")
    repLastName: Optional[str] = Field(None, max_length=100, description="Representative's last name")
    repPhoneNumber: Optional[str] = Field(None, max_length=20, description="Representative's phone number")
    repEmailAddress: Optional[EmailStr] = Field(None, description="Representative's email address")
    repStreetAddress: Optional[str] = Field(None, description="Representative's street address")
    repCity: Optional[str] = Field(None, max_length=100, description="Representative's city")
    repState: Optional[str] = Field(None, max_length=10, description="Representative's state")
    repPostcode: Optional[str] = Field(None, max_length=10, description="Representative's postcode")

    # NDIS Details
    planType: str = Field(..., min_length=1, max_length=50, description="Plan type (plan-managed, self-managed, agency-managed)")
    planManagerName: Optional[str] = Field(None, max_length=100, description="Plan manager name")
    planManagerAgency: Optional[str] = Field(None, max_length=100, description="Plan manager agency")
    ndisNumber: Optional[str] = Field(None, max_length=20, description="NDIS number")
    availableFunding: Optional[str] = Field(None, max_length=100, description="Available funding for capacity building supports")
    planStartDate: date = Field(..., description="Plan start date (YYYY-MM-DD)")
    planReviewDate: date = Field(..., description="Plan review date (YYYY-MM-DD)")
    clientGoals: str = Field(..., min_length=1, description="Client goals as stated in NDIS plan")

    # Referrer Details
    referrerFirstName: str = Field(..., min_length=1, max_length=100, description="Referrer's first name")
    referrerLastName: str = Field(..., min_length=1, max_length=100, description="Referrer's last name")
    referrerAgency: Optional[str] = Field(None, max_length=100, description="Referrer's agency")
    referrerRole: Optional[str] = Field(None, max_length=100, description="Referrer's role")
    referrerEmail: EmailStr = Field(..., description="Referrer's email address")
    referrerPhone: str = Field(..., min_length=1, max_length=20, description="Referrer's phone number")

    # Reason for Referral
    referredFor: str = Field(..., min_length=1, max_length=50, description="What the client is referred for")
    reasonForReferral: str = Field(..., min_length=10, description="Detailed reason for referral")

    # Consent
    consentCheckbox: bool = Field(..., description="Consent obtained from participant")


class ReferralUpdate(BaseModel):
    # Partial update - all fields optional
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    dateOfBirth: Optional[date] = None
    phoneNumber: Optional[str] = None
    emailAddress: Optional[EmailStr] = None
    streetAddress: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    postcode: Optional[str] = None
    preferredContact: Optional[str] = None

    # NDIS Information
    disabilityType: Optional[str] = None
    serviceTypes: Optional[List[str]] = None
    ndisNumber: Optional[str] = None
    urgencyLevel: Optional[str] = None
    preferredContactMethod: Optional[str] = None

    # Support Requirements
    currentSupports: Optional[str] = None
    supportGoals: Optional[str] = None
    accessibilityNeeds: Optional[str] = None
    culturalConsiderations: Optional[str] = None

    # Representative Details
    repFirstName: Optional[str] = None
    repLastName: Optional[str] = None
    repPhoneNumber: Optional[str] = None
    repEmailAddress: Optional[EmailStr] = None
    repRelationship: Optional[str] = None


# ----------------------------
# Response model
# ----------------------------
class ReferralResponse(BaseModel):
    # System / identity
    id: str
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Client Details
    first_name: str
    last_name: str
    date_of_birth: str
    phone_number: str
    email_address: Optional[str] = None
    street_address: str
    city: str
    state: str
    postcode: str
    preferred_contact: str

    # Representative Details
    rep_first_name: Optional[str] = None
    rep_last_name: Optional[str] = None
    rep_phone_number: Optional[str] = None
    rep_email_address: Optional[EmailStr] = None
    rep_street_address: Optional[str] = None
    rep_city: Optional[str] = None
    rep_state: Optional[str] = None
    rep_postcode: Optional[str] = None
    rep_relationship: Optional[str] = None

    # NDIS Details
    plan_type: str
    plan_manager_name: Optional[str] = None
    plan_manager_agency: Optional[str] = None
    ndis_number: Optional[str] = None
    available_funding: Optional[str] = None
    plan_start_date: str
    plan_review_date: str
    client_goals: str

    # Referrer Details
    referrer_first_name: str
    referrer_last_name: str
    referrer_agency: Optional[str] = None
    referrer_role: Optional[str] = None
    referrer_email: str
    referrer_phone: str

    # Reason for Referral
    referred_for: str
    reason_for_referral: str

    # Optional additional info
    disabilityType: Optional[str] = None
    serviceTypes: Optional[List[str]] = None
    urgencyLevel: Optional[str] = None
    preferredContactMethod: Optional[str] = None
    currentSupports: Optional[str] = None
    supportGoals: Optional[str] = None
    accessibilityNeeds: Optional[str] = None
    culturalConsiderations: Optional[str] = None
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
