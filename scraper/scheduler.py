"""
Scheduler for running the job scraper at regular intervals
"""
import schedule
import time
from loguru import logger
from indeed_scraper import main as scrape_jobs

def run_scraper():
    """Run the job scraper"""
    try:
        logger.info("Starting scheduled job scraping...")
        scrape_jobs()
        logger.info("Scheduled job scraping completed successfully")
    except Exception as e:
        logger.error(f"Error in scheduled scraping: {e}")

def main():
    """Main scheduler function"""
    logger.info("Starting job scraper scheduler...")
    
    # Schedule scraping to run daily at 9 AM
    schedule.every().day.at("09:00").do(run_scraper)
    
    # Also run once immediately for testing
    logger.info("Running initial scrape...")
    run_scraper()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
