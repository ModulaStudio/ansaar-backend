from pydantic import BaseModel
from typing import List
import datetime

from app.models import MemberStatus

# County schema
class CountyBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# Location schema
class LocationBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

# Create schema (POST)
class MemberCreate(BaseModel):
    full_name: str
    email: str
    phone: str
    date_of_birth: datetime.date
    profession: str
    skills: List[str]
    referral_source: str
    county_id: int
    location_id: int
    year_joined: str
    consent_to_contact: bool
    emergency_contact_name: str
    emergency_contact_relationship: str
    emergency_contact_phone: str
    status: MemberStatus  # Enum type for status

    class Config:
        orm_mode = True

# Response schema (GET)
class MemberResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str
    date_of_birth: datetime.date
    profession: str
    skills: List[str]
    referral_source: str
    year_joined: str
    consent_to_contact: bool
    emergency_contact_name: str
    emergency_contact_relationship: str
    emergency_contact_phone: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

    # Nested relationships
    county: CountyBase
    location: LocationBase
    status: MemberStatus  # Include status in the response


    class Config:
        orm_mode = True
