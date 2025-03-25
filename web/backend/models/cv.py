from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime


class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    start_date: str
    end_date: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    achievements: Optional[List[str]] = None


class Experience(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    achievements: Optional[List[str]] = None
    technologies: Optional[List[str]] = None


class Skill(BaseModel):
    name: str
    level: Optional[int] = Field(None, ge=1, le=5)
    category: Optional[str] = None
    years_of_experience: Optional[int] = None


class Certificate(BaseModel):
    name: str
    issuer: str
    date_obtained: str
    expiry_date: Optional[str] = None
    credential_id: Optional[str] = None
    credential_url: Optional[str] = None


class Language(BaseModel):
    name: str
    level: str
    certification: Optional[str] = None


class CV(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    summary: Optional[str] = None
    education: List[Education] = []
    experience: List[Experience] = []
    skills: List[Skill] = []
    certificates: Optional[List[Certificate]] = []
    languages: Optional[List[Language]] = []
    website: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    photo_url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    version: Optional[int] = 1
