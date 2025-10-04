"""
Database connection and session management
"""

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import Base
from dotenv import load_dotenv

load_dotenv()

# Database configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# For development, we'll use SQLite for now
# TODO: Set up proper Supabase connection with database password
DATABASE_URL = "sqlite:///./backend/auditor_jobs.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all database tables"""
    Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_database():
    """Initialize database with tables and sample data"""
    create_tables()

    # Add sample data for testing
    db = SessionLocal()
    try:
        from models import Job, AgentMatch, Outreach

        # Check if we already have data
        if db.query(Job).count() > 0:
            return

        # Sample job postings
        sample_jobs = [
            Job(
                title="Senior Auditor",
                company="Deloitte",
                location="New York, NY",
                salary_min=80000,
                salary_max=120000,
                description="We are seeking a Senior Auditor to join our team. Responsibilities include conducting financial audits, reviewing internal controls, and preparing audit reports.",
                url="https://indeed.com/viewjob?jk=sample1",
                source="indeed",
            ),
            Job(
                title="Financial Services Professional",
                company="PwC",
                location="Chicago, IL",
                salary_min=70000,
                salary_max=100000,
                description="Join our Financial Services team as a professional. You will work on client engagements, perform financial analysis, and support audit procedures.",
                url="https://indeed.com/viewjob?jk=sample2",
                source="indeed",
            ),
            Job(
                title="Accounting Manager",
                company="EY",
                location="Los Angeles, CA",
                salary_min=90000,
                salary_max=130000,
                description="We need an Accounting Manager to oversee our accounting operations, manage financial reporting, and ensure compliance with regulations.",
                url="https://indeed.com/viewjob?jk=sample3",
                source="indeed",
            ),
        ]

        for job in sample_jobs:
            db.add(job)

        db.commit()

        # Add sample agent matches
        jobs = db.query(Job).all()
        for job in jobs:
            if "auditor" in job.title.lower():
                match = AgentMatch(
                    job_id=job.id,
                    matched_agent="AFC",
                    confidence_score=0.85,
                    notes="Strong match for AFC agent - involves financial auditing and compliance work",
                )
                db.add(match)
            elif "financial" in job.title.lower():
                match = AgentMatch(
                    job_id=job.id,
                    matched_agent="FSP",
                    confidence_score=0.90,
                    notes="Excellent match for FSP agent - financial services and analysis focus",
                )
                db.add(match)
            else:
                match = AgentMatch(
                    job_id=job.id,
                    matched_agent="other",
                    confidence_score=0.30,
                    notes="Limited automation potential - requires human judgment and management skills",
                )
                db.add(match)

        db.commit()

        # Add sample outreach emails
        for job in jobs[:2]:  # Only for first two jobs
            outreach = Outreach(
                job_id=job.id,
                draft_email=f"""Subject: Automate Your {job.title} Role at 20% of Current Cost

Dear Hiring Manager,

I noticed you're hiring for a {job.title} position at {job.company}. I'm reaching out from Tellen, where we specialize in automating accounting and financial services tasks using AI agents.

Our AI agents can handle many of the responsibilities listed in your job posting at just 20% of the listed salary, with the first month completely free. This includes:

• Financial auditing and compliance work
• Data analysis and reporting
• Process automation and optimization
• 24/7 availability with consistent quality

Would you be interested in a 30-minute call to discuss how we can help reduce your costs while maintaining or improving quality? You can schedule directly here: https://calendly.com/jasonjones/30min-video-chat-with-tellen

Best regards,
Jason Jones
Tellen""",
                status="draft",
                firm_contact="hiring@company.com",
            )
            db.add(outreach)

        db.commit()

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()
