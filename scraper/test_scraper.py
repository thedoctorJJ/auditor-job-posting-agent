"""
Test the Indeed scraper with a small sample
"""
from indeed_scraper import IndeedScraper
from loguru import logger

def test_scraper():
    """Test the scraper with a small search"""
    scraper = IndeedScraper(delay_range=(1, 2), max_retries=2)
    
    # Test with a small search
    logger.info("Testing Indeed scraper...")
    jobs = scraper.search_jobs("auditor", max_pages=1)
    
    logger.info(f"Found {len(jobs)} jobs")
    
    for job in jobs[:3]:  # Show first 3 jobs
        logger.info(f"Job: {job.get('title', 'Unknown')} at {job.get('company', 'Unknown')}")
        logger.info(f"Salary: ${job.get('salary_min', 'N/A')} - ${job.get('salary_max', 'N/A')}")
        logger.info(f"URL: {job.get('url', 'N/A')}")
        logger.info("---")
    
    # Test saving to database
    if jobs:
        saved_count = scraper.save_jobs_to_db(jobs[:2])  # Save first 2 jobs
        logger.info(f"Saved {saved_count} jobs to database")

if __name__ == "__main__":
    test_scraper()
