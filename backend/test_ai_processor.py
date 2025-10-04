"""
Test the AI processor with mock data
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Job, AgentMatch
from loguru import logger


def test_heuristic_matching():
    """Test the heuristic matching logic"""
    db = SessionLocal()
    try:
        # Get some jobs from the database
        jobs = db.query(Job).limit(5).all()
        
        logger.info(f"Testing heuristic matching on {len(jobs)} jobs")
        
        for job in jobs:
            logger.info(f"\nJob: {job.title} at {job.company}")
            logger.info(f"Description: {job.description[:100]}...")
            
            # Simple heuristic matching
            title_lower = job.title.lower()
            desc_lower = job.description.lower() if job.description else ""
            
            # AFC matching criteria
            afc_keywords = ["audit", "compliance", "internal control", "risk", "regulatory", "financial statement"]
            afc_score = sum(1 for keyword in afc_keywords if keyword in title_lower or keyword in desc_lower)
            
            # FSP matching criteria
            fsp_keywords = ["financial analysis", "investment", "portfolio", "market research", "financial modeling", "data analysis"]
            fsp_score = sum(1 for keyword in fsp_keywords if keyword in title_lower or keyword in desc_lower)
            
            if afc_score > fsp_score and afc_score > 0:
                confidence = min(0.9, 0.5 + (afc_score * 0.1))
                matched_agent = "AFC"
                explanation = f"Job matches AFC agent based on {afc_score} audit/compliance keywords"
            elif fsp_score > 0:
                confidence = min(0.9, 0.5 + (fsp_score * 0.1))
                matched_agent = "FSP"
                explanation = f"Job matches FSP agent based on {fsp_score} financial analysis keywords"
            else:
                matched_agent = "other"
                confidence = 0.3
                explanation = "Job requires human judgment and management skills"
            
            logger.info(f"Matched Agent: {matched_agent}")
            logger.info(f"Confidence: {confidence}")
            logger.info(f"Explanation: {explanation}")
            
            # Check if match already exists
            existing_match = db.query(AgentMatch).filter(AgentMatch.job_id == job.id).first()
            if existing_match:
                logger.info(f"Already has match: {existing_match.matched_agent} (confidence: {existing_match.confidence_score})")
            else:
                logger.info("No existing match - would create new match")
        
    except Exception as e:
        logger.error(f"Error in test: {e}")
    finally:
        db.close()


def create_mock_matches():
    """Create mock agent matches for testing"""
    db = SessionLocal()
    try:
        # Get jobs without matches
        processed_job_ids = db.query(AgentMatch.job_id).distinct().all()
        processed_job_ids = [job_id[0] for job_id in processed_job_ids]
        
        unprocessed_jobs = db.query(Job).filter(~Job.id.in_(processed_job_ids)).all()
        
        logger.info(f"Creating mock matches for {len(unprocessed_jobs)} jobs")
        
        for job in unprocessed_jobs:
            # Simple heuristic matching
            title_lower = job.title.lower()
            desc_lower = job.description.lower() if job.description else ""
            
            # AFC matching criteria
            afc_keywords = ["audit", "compliance", "internal control", "risk", "regulatory", "financial statement"]
            afc_score = sum(1 for keyword in afc_keywords if keyword in title_lower or keyword in desc_lower)
            
            # FSP matching criteria
            fsp_keywords = ["financial analysis", "investment", "portfolio", "market research", "financial modeling", "data analysis"]
            fsp_score = sum(1 for keyword in fsp_keywords if keyword in title_lower or keyword in desc_lower)
            
            if afc_score > fsp_score and afc_score > 0:
                confidence = min(0.9, 0.5 + (afc_score * 0.1))
                matched_agent = "AFC"
                explanation = f"Job matches AFC agent based on {afc_score} audit/compliance keywords"
            elif fsp_score > 0:
                confidence = min(0.9, 0.5 + (fsp_score * 0.1))
                matched_agent = "FSP"
                explanation = f"Job matches FSP agent based on {fsp_score} financial analysis keywords"
            else:
                matched_agent = "other"
                confidence = 0.3
                explanation = "Job requires human judgment and management skills"
            
            # Create agent match
            agent_match = AgentMatch(
                job_id=job.id,
                matched_agent=matched_agent,
                confidence_score=confidence,
                notes=explanation
            )
            
            db.add(agent_match)
            logger.info(f"Created match for {job.title}: {matched_agent} (confidence: {confidence})")
        
        db.commit()
        logger.info("Successfully created mock agent matches")
        
    except Exception as e:
        logger.error(f"Error creating mock matches: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    logger.info("Testing AI processor...")
    test_heuristic_matching()
    
    logger.info("\nCreating mock matches...")
    create_mock_matches()
    
    logger.info("Test completed!")
