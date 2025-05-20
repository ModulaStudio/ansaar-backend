from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP, Enum, Date, JSON, func
from sqlalchemy.orm import relationship
from .database import Base
import enum


# Define the Enum for status
class MemberStatus(enum.Enum):
    active = 'active'
    inactive = 'inactive'

class County(Base):
    __tablename__ = "counties"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    
    locations = relationship("Location", back_populates="county")
    members = relationship("Member", back_populates="county")

class Location(Base):
    __tablename__ = "locations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    county_id = Column(Integer, ForeignKey("counties.id"))
    
    county = relationship("County", back_populates="locations")
    members = relationship("Member", back_populates="location")

class Member(Base):
    __tablename__ = "members"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    date_of_birth = Column(Date)
    profession = Column(String)
    skills = Column(JSON)
    referral_source = Column(String)
    county_id = Column(Integer, ForeignKey("counties.id"))
    location_id = Column(Integer, ForeignKey("locations.id"))
    year_joined = Column(String)  # Kept as string to match frontend dropdown options
    consent_to_contact = Column(Boolean, default=False)
    emergency_contact_name = Column(String)
    emergency_contact_relationship = Column(String)
    emergency_contact_phone = Column(String)
    status = Column(Enum(MemberStatus), nullable=False, default=MemberStatus.active)  # Enum status
    created_at = Column(TIMESTAMP, default=func.now())
    updated_at = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
    
    # Relationships
    county = relationship("County", back_populates="members")
    location = relationship("Location", back_populates="members")
