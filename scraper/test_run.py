"""
Test run with 10 job postings
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mock_scraper import MockIndeedScraper
from loguru import logger


def main():
    """Generate exactly 10 test jobs"""
    scraper = MockIndeedScraper()

    logger.info("Generating 10 test job postings...")
    jobs = scraper.generate_mock_jobs(count=10)

    logger.info(f"Generated {len(jobs)} test jobs")

    # Show the jobs
    for i, job in enumerate(jobs, 1):
        logger.info(f"{i}. {job['title']} at {job['company']} - ${job['salary_min']:,.0f}-${job['salary_max']:,.0f}")

    # Save to database
    saved_count = scraper.save_jobs_to_db(jobs)
    logger.info(f"Test run completed. Saved {saved_count} new jobs to database.")

    return saved_count


if __name__ == "__main__":
    main()
