"""
Database model tests
"""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, Job, AgentMatch, Outreach

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Create test database session"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_job_creation(db_session):
    """Test job model creation"""
    job = Job(
        title="Test Auditor",
        company="Test Company",
        location="Test City",
        salary_min=50000,
        salary_max=70000,
        description="Test job description",
        url="https://test.com/job",
        source="Test Source"
    )
    db_session.add(job)
    db_session.commit()
    
    assert job.id is not None
    assert job.title == "Test Auditor"
    assert job.company == "Test Company"

def test_agent_match_creation(db_session):
    """Test agent match model creation"""
    # Create a job first
    job = Job(
        title="Test Job",
        company="Test Company",
        location="Test City",
        salary_min=50000,
        salary_max=70000,
        description="Test description",
        url="https://test.com",
        source="Test"
    )
    db_session.add(job)
    db_session.commit()
    
    # Create agent match
    match = AgentMatch(
        job_id=job.id,
        matched_agent="AFC",
        confidence_score=0.85
    )
    db_session.add(match)
    db_session.commit()
    
    assert match.id is not None
    assert match.matched_agent == "AFC"
    assert match.confidence_score == 0.85
