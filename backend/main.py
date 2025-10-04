"""
FastAPI main application
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from dotenv import load_dotenv

from database import get_db, init_database
from models import Job, AgentMatch, Outreach, JobResponse, AgentMatchResponse, OutreachResponse

load_dotenv()

app = FastAPI(
    title="Auditor Job Posting Agent API",
    description="AI-powered job posting analysis and outreach system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_database()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Auditor Job Posting Agent API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "auditor-job-posting-agent"}

# Job endpoints
@app.get("/jobs", response_model=List[JobResponse])
async def get_jobs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all job postings with pagination"""
    jobs = db.query(Job).offset(skip).limit(limit).all()
    return jobs

@app.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get a specific job posting"""
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@app.get("/jobs/{job_id}/matches", response_model=List[AgentMatchResponse])
async def get_job_matches(job_id: int, db: Session = Depends(get_db)):
    """Get agent matches for a specific job"""
    matches = db.query(AgentMatch).filter(AgentMatch.job_id == job_id).all()
    return matches

# Agent match endpoints
@app.get("/agent-matches", response_model=List[AgentMatchResponse])
async def get_agent_matches(
    agent: Optional[str] = None,
    min_confidence: Optional[float] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get agent matches with optional filtering"""
    query = db.query(AgentMatch)
    
    if agent:
        query = query.filter(AgentMatch.matched_agent == agent)
    
    if min_confidence:
        query = query.filter(AgentMatch.confidence_score >= min_confidence)
    
    matches = query.offset(skip).limit(limit).all()
    return matches

# Outreach endpoints
@app.get("/outreach", response_model=List[OutreachResponse])
async def get_outreach_emails(
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get outreach emails with optional status filtering"""
    query = db.query(Outreach)
    
    if status:
        query = query.filter(Outreach.status == status)
    
    emails = query.offset(skip).limit(limit).all()
    return emails

@app.get("/outreach/{outreach_id}", response_model=OutreachResponse)
async def get_outreach_email(outreach_id: int, db: Session = Depends(get_db)):
    """Get a specific outreach email"""
    email = db.query(Outreach).filter(Outreach.id == outreach_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Outreach email not found")
    return email

@app.put("/outreach/{outreach_id}/approve")
async def approve_outreach_email(outreach_id: int, db: Session = Depends(get_db)):
    """Approve an outreach email for sending"""
    email = db.query(Outreach).filter(Outreach.id == outreach_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Outreach email not found")
    
    email.status = "approved"
    db.commit()
    
    return {"message": "Outreach email approved", "id": outreach_id}

@app.put("/outreach/{outreach_id}/reject")
async def reject_outreach_email(outreach_id: int, db: Session = Depends(get_db)):
    """Reject an outreach email"""
    email = db.query(Outreach).filter(Outreach.id == outreach_id).first()
    if not email:
        raise HTTPException(status_code=404, detail="Outreach email not found")
    
    email.status = "rejected"
    db.commit()
    
    return {"message": "Outreach email rejected", "id": outreach_id}

# Statistics endpoints
@app.get("/stats")
async def get_statistics(db: Session = Depends(get_db)):
    """Get system statistics"""
    total_jobs = db.query(Job).count()
    total_matches = db.query(AgentMatch).count()
    total_outreach = db.query(Outreach).count()
    
    # Agent distribution
    afc_matches = db.query(AgentMatch).filter(AgentMatch.matched_agent == "AFC").count()
    fsp_matches = db.query(AgentMatch).filter(AgentMatch.matched_agent == "FSP").count()
    other_matches = db.query(AgentMatch).filter(AgentMatch.matched_agent == "other").count()
    
    # Outreach status distribution
    draft_outreach = db.query(Outreach).filter(Outreach.status == "draft").count()
    approved_outreach = db.query(Outreach).filter(Outreach.status == "approved").count()
    sent_outreach = db.query(Outreach).filter(Outreach.status == "sent").count()
    rejected_outreach = db.query(Outreach).filter(Outreach.status == "rejected").count()
    
    return {
        "jobs": {
            "total": total_jobs
        },
        "agent_matches": {
            "total": total_matches,
            "afc": afc_matches,
            "fsp": fsp_matches,
            "other": other_matches
        },
        "outreach": {
            "total": total_outreach,
            "draft": draft_outreach,
            "approved": approved_outreach,
            "sent": sent_outreach,
            "rejected": rejected_outreach
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
