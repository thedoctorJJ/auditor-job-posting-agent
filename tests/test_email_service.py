"""
Email service tests
"""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from unittest.mock import Mock, patch
from backend.email_service import EmailService
from backend.models import Job, AgentMatch

@pytest.fixture
def sample_job():
    """Create a sample job for testing"""
    return Job(
        id=1,
        title="Senior Auditor",
        company="Test Company",
        location="Test City",
        salary_min=80000,
        salary_max=120000,
        description="Conduct financial audits and compliance reviews",
        url="https://test.com/job",
        source="Test Source"
    )

@pytest.fixture
def sample_agent_match():
    """Create a sample agent match for testing"""
    return AgentMatch(
        id=1,
        job_id=1,
        matched_agent="AFC",
        confidence_score=0.85
    )

@pytest.fixture
def email_service():
    """Create email service instance for testing"""
    return EmailService()

def test_generate_outreach_email(email_service, sample_job, sample_agent_match):
    """Test outreach email generation"""
    email_content = email_service.generate_outreach_email(sample_job, sample_agent_match)
    
    # Check that email contains key elements
    assert "Senior Auditor" in email_content
    assert "Test Company" in email_content
    assert "Accounting & Financial Compliance agent" in email_content
    assert "20,000" in email_content  # 20% of average salary
    assert "Subject:" in email_content

def test_extract_key_tasks(email_service):
    """Test key task extraction from job description"""
    description = "Conduct financial audits, perform analysis, and ensure compliance"
    tasks = email_service._extract_key_tasks(description)
    
    assert "audit" in tasks.lower()
    assert "analysis" in tasks.lower()
    assert "compliance" in tasks.lower()

def test_save_outreach_draft(email_service, sample_job):
    """Test saving outreach draft to database"""
    with patch('backend.email_service.SessionLocal') as mock_session:
        mock_db = Mock()
        mock_outreach = Mock()
        mock_outreach.id = 1
        mock_db.add.return_value = mock_outreach
        mock_db.refresh.return_value = mock_outreach
        mock_session.return_value.__enter__.return_value = mock_db
        
        email_content = "Test email content"
        outreach_id = email_service.save_outreach_draft(1, email_content, "test@example.com")
        
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        assert outreach_id == 1

@patch('backend.email_service.smtplib.SMTP')
def test_send_email_success(mock_smtp, email_service):
    """Test successful email sending"""
    # Create a new email service instance with mocked credentials
    email_service.email_username = 'test@example.com'
    email_service.email_password = 'password'
    email_service.from_email = 'from@example.com'
    email_service.from_name = 'Test Name'
    
    mock_server = Mock()
    mock_smtp.return_value = mock_server
    
    result = email_service.send_email("to@example.com", "Test Subject", "Test Body")
    
    assert result is True
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()
    mock_server.sendmail.assert_called_once()

def test_send_email_no_credentials(email_service):
    """Test email sending without credentials"""
    result = email_service.send_email("to@example.com", "Test Subject", "Test Body")
    assert result is False
