"""
Indeed job scraper with retry logic and error handling
"""

import time
import random
import re
from datetime import datetime
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse, parse_qs

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from loguru import logger

import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import Job


class IndeedScraper:
    """Indeed job scraper with retry logic and respectful scraping"""

    def __init__(self, delay_range=(2, 5), max_retries=3):
        self.delay_range = delay_range
        self.max_retries = max_retries
        self.session = requests.Session()
        self.ua = UserAgent()
        self.setup_session()

    def setup_session(self):
        """Setup requests session with headers"""
        self.session.headers.update(
            {
                "User-Agent": self.ua.random,
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                "Accept-Encoding": "gzip, deflate",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
            }
        )

    def get_selenium_driver(self):
        """Get configured Selenium WebDriver"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument(f"--user-agent={self.ua.random}")

        driver = webdriver.Chrome(
            service=webdriver.chrome.service.Service(ChromeDriverManager().install()), options=chrome_options
        )
        return driver

    def delay(self):
        """Random delay between requests"""
        delay = random.uniform(*self.delay_range)
        logger.info(f"Waiting {delay:.2f} seconds...")
        time.sleep(delay)

    def extract_salary(self, text: str) -> tuple[Optional[float], Optional[float]]:
        """Extract salary range from text"""
        if not text:
            return None, None

        # Common salary patterns
        patterns = [
            r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*-\s*\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",  # $50,000 - $70,000
            r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*to\s*\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",  # $50,000 to $70,000
            r"(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*-\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",  # 50,000 - 70,000
            r"(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\s*to\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)",  # 50,000 to 70,000
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    min_sal = float(match.group(1).replace(",", ""))
                    max_sal = float(match.group(2).replace(",", ""))
                    return min_sal, max_sal
                except ValueError:
                    continue

        # Single salary
        single_pattern = r"\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)"
        match = re.search(single_pattern, text)
        if match:
            try:
                salary = float(match.group(1).replace(",", ""))
                return salary, salary
            except ValueError:
                pass

        return None, None

    def scrape_job_listing(self, job_url: str) -> Optional[Dict]:
        """Scrape individual job listing"""
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Scraping job: {job_url} (attempt {attempt + 1})")

                response = self.session.get(job_url, timeout=30)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, "html.parser")

                # Extract job details
                job_data = {"url": job_url, "source": "indeed"}

                # Job title
                title_elem = soup.find("h1", class_="jobsearch-JobInfoHeader-title")
                if not title_elem:
                    title_elem = soup.find("h1")
                if title_elem:
                    job_data["title"] = title_elem.get_text(strip=True)

                # Company name
                company_elem = soup.find("div", {"data-testid": "company-name"})
                if not company_elem:
                    company_elem = soup.find("a", {"data-testid": "company-name"})
                if not company_elem:
                    company_elem = soup.find("span", class_="jobsearch-CompanyReview--heading")
                if company_elem:
                    job_data["company"] = company_elem.get_text(strip=True)

                # Location
                location_elem = soup.find("div", {"data-testid": "job-location"})
                if not location_elem:
                    location_elem = soup.find("div", class_="jobsearch-JobInfoHeader-subtitle")
                if location_elem:
                    job_data["location"] = location_elem.get_text(strip=True)

                # Job description
                desc_elem = soup.find("div", {"id": "jobDescriptionText"})
                if not desc_elem:
                    desc_elem = soup.find("div", class_="jobsearch-jobDescriptionText")
                if desc_elem:
                    job_data["description"] = desc_elem.get_text(strip=True)

                # Salary (look in multiple places)
                salary_text = ""
                salary_elem = soup.find("div", {"data-testid": "salary-snippet-container"})
                if salary_elem:
                    salary_text = salary_elem.get_text(strip=True)
                else:
                    # Look for salary in job description
                    if job_data.get("description"):
                        salary_match = re.search(r"salary[:\s]*([^.]*)", job_data["description"], re.IGNORECASE)
                        if salary_match:
                            salary_text = salary_match.group(1)

                if salary_text:
                    min_sal, max_sal = self.extract_salary(salary_text)
                    job_data["salary_min"] = min_sal
                    job_data["salary_max"] = max_sal

                # Posting date
                date_elem = soup.find("span", {"data-testid": "myJobsStateDate"})
                if date_elem:
                    date_text = date_elem.get_text(strip=True)
                    # Parse relative dates like "2 days ago"
                    if "day" in date_text:
                        days = int(re.search(r"(\d+)", date_text).group(1))
                        job_data["date_posted"] = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                    else:
                        job_data["date_posted"] = datetime.now()
                else:
                    job_data["date_posted"] = datetime.now()

                logger.info(f"Successfully scraped job: {job_data.get('title', 'Unknown')}")
                return job_data

            except Exception as e:
                logger.error(f"Error scraping job {job_url} (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    self.delay()
                else:
                    logger.error(f"Failed to scrape job after {self.max_retries} attempts: {job_url}")
                    return None

    def search_jobs(self, query: str, location: str = "", max_pages: int = 3) -> List[Dict]:
        """Search for jobs on Indeed"""
        all_jobs = []

        for page in range(max_pages):
            try:
                logger.info(f"Searching Indeed page {page + 1} for: {query}")

                # Build search URL
                params = {"q": query, "l": location, "start": page * 10, "sort": "date"}

                search_url = "https://www.indeed.com/jobs"
                response = self.session.get(search_url, params=params, timeout=30)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, "html.parser")

                # Find job links
                job_links = []
                job_cards = soup.find_all("div", {"data-testid": "job-title"})

                for card in job_cards:
                    link_elem = card.find("a")
                    if link_elem and link_elem.get("href"):
                        job_url = urljoin("https://www.indeed.com", link_elem["href"])
                        job_links.append(job_url)

                logger.info(f"Found {len(job_links)} job links on page {page + 1}")

                # Scrape each job
                for job_url in job_links:
                    job_data = self.scrape_job_listing(job_url)
                    if job_data:
                        all_jobs.append(job_data)
                    self.delay()

                # Delay between pages
                if page < max_pages - 1:
                    self.delay()

            except Exception as e:
                logger.error(f"Error searching page {page + 1}: {e}")
                continue

        logger.info(f"Total jobs scraped: {len(all_jobs)}")
        return all_jobs

    def save_jobs_to_db(self, jobs: List[Dict]) -> int:
        """Save scraped jobs to database"""
        db = SessionLocal()
        saved_count = 0

        try:
            for job_data in jobs:
                # Check if job already exists
                existing_job = db.query(Job).filter(Job.url == job_data["url"]).first()
                if existing_job:
                    logger.info(f"Job already exists: {job_data.get('title', 'Unknown')}")
                    continue

                # Create new job
                job = Job(**job_data)
                db.add(job)
                saved_count += 1
                logger.info(f"Saved job: {job_data.get('title', 'Unknown')}")

            db.commit()
            logger.info(f"Successfully saved {saved_count} new jobs to database")

        except Exception as e:
            logger.error(f"Error saving jobs to database: {e}")
            db.rollback()
        finally:
            db.close()

        return saved_count


def main():
    """Main scraping function"""
    scraper = IndeedScraper()

    # Search terms for accounting/auditing jobs
    search_terms = [
        "auditor",
        "accounting",
        "financial analyst",
        "bookkeeper",
        "tax preparer",
        "financial services",
        "compliance",
        "internal audit",
    ]

    all_jobs = []

    for term in search_terms:
        logger.info(f"Searching for: {term}")
        jobs = scraper.search_jobs(term, max_pages=2)
        all_jobs.extend(jobs)

        # Delay between search terms
        scraper.delay()

    # Remove duplicates based on URL
    unique_jobs = []
    seen_urls = set()
    for job in all_jobs:
        if job["url"] not in seen_urls:
            unique_jobs.append(job)
            seen_urls.add(job["url"])

    logger.info(f"Found {len(unique_jobs)} unique jobs")

    # Save to database
    saved_count = scraper.save_jobs_to_db(unique_jobs)
    logger.info(f"Scraping completed. Saved {saved_count} new jobs.")


if __name__ == "__main__":
    main()
