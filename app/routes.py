from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from . import models
from .database import SessionLocal
from .schemas import MemberCreate, MemberResponse
from typing import List

router = APIRouter()

# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------- ROUTES -------------------

# Get all counties
@router.get("/counties")
def get_counties(db: Session = Depends(get_db)):
    return db.query(models.County).all()

# Get locations by county_id
@router.get("/locations/{county_id}")
def get_locations(county_id: int, db: Session = Depends(get_db)):
    return db.query(models.Location).filter(models.Location.county_id == county_id).all()

# Get all members with county and location info
@router.get("/members", response_model=List[MemberResponse])
def get_members(db: Session = Depends(get_db)):
    members = db.query(models.Member)\
        .options(joinedload(models.Member.county), joinedload(models.Member.location))\
        .all()
    return members

# Create a new member
@router.post("/members", response_model=MemberResponse)
def create_member(member: MemberCreate, db: Session = Depends(get_db)):
    # Validate county
    county = db.query(models.County).filter(models.County.id == member.county_id).first()
    if not county:
        raise HTTPException(status_code=404, detail="County not found")

    # Validate location
    location = db.query(models.Location).filter(models.Location.id == member.location_id).first()
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    db_member = models.Member(
        full_name=member.full_name,
        email=member.email,
        phone=member.phone,
        date_of_birth=member.date_of_birth,
        profession=member.profession,
        skills=member.skills,
        referral_source=member.referral_source,
        county_id=member.county_id,
        location_id=member.location_id,
        year_joined=member.year_joined,
        consent_to_contact=member.consent_to_contact,
        emergency_contact_name=member.emergency_contact_name,
        emergency_contact_relationship=member.emergency_contact_relationship,
        emergency_contact_phone=member.emergency_contact_phone,
        status=member.status,
    )

    db.add(db_member)
    db.commit()
    db.refresh(db_member)

    return db_member
