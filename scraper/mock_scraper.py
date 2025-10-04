"""
Mock scraper for development and testing when real scraping is blocked
"""
import random
from datetime import datetime, timedelta
from typing import List, Dict
from loguru import logger

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import Job


class MockIndeedScraper:
    """Mock Indeed scraper for development and testing"""
    
    def __init__(self):
        self.companies = [
            "Deloitte", "PwC", "EY", "KPMG", "Grant Thornton",
            "RSM", "BDO", "Crowe", "Baker Tilly", "Moss Adams",
            "CliftonLarsonAllen", "CBIZ", "Marcum", "Weaver",
            "Cherry Bekaert", "Dixon Hughes Goodman", "Plante Moran"
        ]
        
        self.job_titles = [
            "Senior Auditor", "Staff Auditor", "Internal Auditor",
            "Financial Analyst", "Senior Financial Analyst",
            "Accounting Manager", "Senior Accountant", "Staff Accountant",
            "Tax Senior", "Tax Manager", "Compliance Analyst",
            "Financial Services Professional", "Risk Analyst",
            "Forensic Accountant", "Cost Accountant", "Revenue Analyst"
        ]
        
        self.locations = [
            "New York, NY", "Chicago, IL", "Los Angeles, CA",
            "Houston, TX", "Phoenix, AZ", "Philadelphia, PA",
            "San Antonio, TX", "San Diego, CA", "Dallas, TX",
            "San Jose, CA", "Austin, TX", "Jacksonville, FL",
            "Fort Worth, TX", "Columbus, OH", "Charlotte, NC"
        ]
        
        self.salary_ranges = [
            (45000, 65000), (55000, 75000), (65000, 85000),
            (75000, 95000), (85000, 110000), (95000, 125000),
            (110000, 140000), (125000, 160000)
        ]
    
    def generate_mock_jobs(self, count: int = 10) -> List[Dict]:
        """Generate mock job postings"""
        jobs = []
        
        for i in range(count):
            title = random.choice(self.job_titles)
            company = random.choice(self.companies)
            location = random.choice(self.locations)
            salary_min, salary_max = random.choice(self.salary_ranges)
            
            # Add some variation to salaries
            salary_min += random.randint(-5000, 5000)
            salary_max += random.randint(-5000, 5000)
            
            # Generate job description
            description = self.generate_job_description(title, company)
            
            # Generate posting date (within last 30 days)
            days_ago = random.randint(0, 30)
            date_posted = datetime.now() - timedelta(days=days_ago)
            
            job = {
                'title': title,
                'company': company,
                'location': location,
                'salary_min': salary_min,
                'salary_max': salary_max,
                'description': description,
                'url': f"https://indeed.com/viewjob?jk=mock{i:06d}",
                'source': 'indeed',
                'date_posted': date_posted
            }
            
            jobs.append(job)
        
        return jobs
    
    def generate_job_description(self, title: str, company: str) -> str:
        """Generate realistic job description"""
        descriptions = {
            'auditor': f"""
{company} is seeking a {title} to join our growing team. The ideal candidate will:

• Conduct financial and operational audits
• Review internal controls and compliance procedures
• Prepare detailed audit reports and recommendations
• Work with cross-functional teams to implement improvements
• Ensure compliance with regulatory requirements
• Analyze financial data and identify areas for improvement

Requirements:
• Bachelor's degree in Accounting, Finance, or related field
• CPA certification preferred
• 2-5 years of audit experience
• Strong analytical and communication skills
• Proficiency in Excel and audit software
• Ability to work independently and as part of a team

We offer competitive salary, comprehensive benefits, and opportunities for professional growth.
            """,
            'financial': f"""
{company} is looking for a {title} to support our financial services division. Responsibilities include:

• Perform financial analysis and modeling
• Prepare monthly and quarterly financial reports
• Assist with budgeting and forecasting processes
• Support client engagements and presentations
• Conduct market research and competitive analysis
• Collaborate with internal teams on financial projects

Qualifications:
• Bachelor's degree in Finance, Economics, or related field
• 1-4 years of financial analysis experience
• Strong Excel and financial modeling skills
• Knowledge of financial software and databases
• Excellent written and verbal communication skills
• Detail-oriented with strong analytical abilities

Join our dynamic team and advance your career in financial services.
            """,
            'accounting': f"""
{company} has an exciting opportunity for a {title}. The role involves:

• Manage day-to-day accounting operations
• Prepare and review financial statements
• Oversee accounts payable and receivable processes
• Ensure compliance with accounting standards
• Coordinate with external auditors
• Lead accounting team and provide guidance

Requirements:
• Bachelor's degree in Accounting required
• CPA certification strongly preferred
• 3-7 years of progressive accounting experience
• Experience with accounting software (QuickBooks, SAP, etc.)
• Strong leadership and management skills
• Knowledge of GAAP and financial reporting standards

We provide excellent benefits, professional development opportunities, and a collaborative work environment.
            """
        }
        
        # Determine description type based on title
        if 'audit' in title.lower():
            desc_type = 'auditor'
        elif 'financial' in title.lower():
            desc_type = 'financial'
        else:
            desc_type = 'accounting'
        
        return descriptions[desc_type].strip()
    
    def save_jobs_to_db(self, jobs: List[Dict]) -> int:
        """Save mock jobs to database"""
        # Import here to ensure we're using the right database path
        from backend.database import SessionLocal
        db = SessionLocal()
        saved_count = 0
        
        try:
            for job_data in jobs:
                # Check if job already exists
                existing_job = db.query(Job).filter(Job.url == job_data['url']).first()
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
    """Main function to generate and save mock jobs"""
    scraper = MockIndeedScraper()
    
    logger.info("Generating mock job postings...")
    jobs = scraper.generate_mock_jobs(count=15)
    
    logger.info(f"Generated {len(jobs)} mock jobs")
    
    # Save to database
    saved_count = scraper.save_jobs_to_db(jobs)
    logger.info(f"Mock scraping completed. Saved {saved_count} new jobs.")


if __name__ == "__main__":
    main()
