"""
Test database functionality
"""
from database import SessionLocal, get_db
from models import Job, AgentMatch, Outreach

def test_database():
    """Test database operations"""
    db = SessionLocal()
    try:
        # Test job retrieval
        jobs = db.query(Job).all()
        print(f"Found {len(jobs)} jobs in database")
        
        for job in jobs:
            print(f"- {job.title} at {job.company} (${job.salary_min}-${job.salary_max})")
            
            # Test agent matches
            matches = db.query(AgentMatch).filter(AgentMatch.job_id == job.id).all()
            for match in matches:
                print(f"  Agent Match: {match.matched_agent} (confidence: {match.confidence_score})")
            
            # Test outreach emails
            outreach = db.query(Outreach).filter(Outreach.job_id == job.id).all()
            for email in outreach:
                print(f"  Outreach Status: {email.status}")
        
        print("\nDatabase test completed successfully!")
        
    except Exception as e:
        print(f"Database test failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_database()
