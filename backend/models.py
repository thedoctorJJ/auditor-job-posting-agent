"""
Database models for the Auditor Job Posting Agent
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pydantic import BaseModel

Base = declarative_base()


class Job(Base):
    """Job posting model"""
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    company = Column(String(255), nullable=False, index=True)
    location = Column(String(255), nullable=True, index=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    description = Column(Text, nullable=True)
    url = Column(String(500), nullable=False, unique=True)
    source = Column(String(100), nullable=False, default="indeed")
    date_posted = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    agent_matches = relationship("AgentMatch", back_populates="job", cascade="all, delete-orphan")
    outreach_emails = relationship("Outreach", back_populates="job", cascade="all, delete-orphan")


class AgentMatch(Base):
    """Agent matching results model"""
    __tablename__ = "agent_matches"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    matched_agent = Column(String(100), nullable=False, index=True)  # AFC, FSP, other
    confidence_score = Column(Float, nullable=False)  # 0-1 scale
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    job = relationship("Job", back_populates="agent_matches")


class Outreach(Base):
    """Outreach email model"""
    __tablename__ = "outreach"
    
    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)
    draft_email = Column(Text, nullable=False)
    status = Column(String(50), nullable=False, default="draft")  # draft, sent, rejected
    firm_contact = Column(String(255), nullable=True)
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    job = relationship("Job", back_populates="outreach_emails")


# Pydantic models for API serialization
class JobBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    description: Optional[str] = None
    url: str
    source: str = "indeed"


class JobCreate(JobBase):
    pass


class JobResponse(JobBase):
    id: int
    date_posted: datetime
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AgentMatchBase(BaseModel):
    matched_agent: str
    confidence_score: float
    notes: Optional[str] = None


class AgentMatchCreate(AgentMatchBase):
    job_id: int


class AgentMatchResponse(AgentMatchBase):
    id: int
    job_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class OutreachBase(BaseModel):
    draft_email: str
    status: str = "draft"
    firm_contact: Optional[str] = None


class OutreachCreate(OutreachBase):
    job_id: int


class OutreachResponse(OutreachBase):
    id: int
    job_id: int
    sent_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class JobWithMatches(JobResponse):
    agent_matches: list[AgentMatchResponse] = []
    outreach_emails: list[OutreachResponse] = []
