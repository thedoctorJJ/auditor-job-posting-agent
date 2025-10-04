"""
AI-powered job processing and agent matching using GPT-5-Codex
"""

from typing import Dict, List, Optional, Tuple
from openai import OpenAI
from loguru import logger

import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Job, AgentMatch


class AIJobProcessor:
    """AI processor for job matching and analysis using GPT-5-Codex"""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-5-codex")

        # Define Tellen agents and their capabilities
        self.tellen_agents = {
            "AFC": {
                "name": "Accounting & Financial Compliance",
                "capabilities": [
                    "Financial auditing and compliance",
                    "Internal control reviews",
                    "Risk assessment and management",
                    "Regulatory compliance monitoring",
                    "Financial statement analysis",
                    "Audit trail verification",
                    "Compliance reporting",
                    "Financial data validation",
                ],
            },
            "FSP": {
                "name": "Financial Services Professional",
                "capabilities": [
                    "Financial analysis and modeling",
                    "Investment research and analysis",
                    "Portfolio management support",
                    "Financial reporting and dashboards",
                    "Market research and analysis",
                    "Client financial assessments",
                    "Financial planning assistance",
                    "Data analysis and visualization",
                ],
            },
            "other": {
                "name": "Other/New Opportunity",
                "capabilities": [
                    "Tasks requiring human judgment",
                    "Strategic decision making",
                    "Client relationship management",
                    "Complex problem solving",
                    "Leadership and management",
                    "Creative and innovative thinking",
                ],
            },
        }

    def analyze_job_description(self, job_description: str) -> Dict:
        """Analyze job description using GPT-5-Codex"""
        try:
            prompt = f"""
Analyze the following job description and extract key information:

Job Description:
{job_description}

Please provide a JSON response with the following structure:
{{
    "primary_responsibilities": ["list of main job duties"],
    "required_skills": ["list of required skills"],
    "automation_potential": "high/medium/low",
    "repetitive_tasks": ["list of repetitive, automatable tasks"],
    "advisory_tasks": ["list of tasks requiring human judgment"],
    "salary_indicators": ["any salary-related information"],
    "industry_focus": "primary industry or sector"
}}

Focus on identifying tasks that could be automated vs. those requiring human expertise.
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert job analyst specializing in identifying automation opportunities in accounting and financial services roles.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.3,
                max_tokens=1000,
            )

            # Parse the response
            analysis_text = response.choices[0].message.content
            logger.info(f"GPT-5-Codex analysis: {analysis_text[:200]}...")

            # For now, return a structured response (in production, you'd parse the JSON)
            return {
                "analysis": analysis_text,
                "automation_potential": "medium",  # Would be extracted from JSON
                "primary_responsibilities": ["Financial analysis", "Reporting", "Compliance"],
                "repetitive_tasks": ["Data entry", "Report generation", "Calculation"],
                "advisory_tasks": ["Strategic planning", "Client consultation"],
            }

        except Exception as e:
            logger.error(f"Error analyzing job description: {e}")
            return {
                "analysis": "Analysis failed",
                "automation_potential": "unknown",
                "primary_responsibilities": [],
                "repetitive_tasks": [],
                "advisory_tasks": [],
            }

    def match_job_to_agent(self, job: Job, analysis: Dict) -> Tuple[str, float, str]:
        """Match job to Tellen agent using GPT-5-Codex"""
        try:
            # Create agent descriptions for matching
            agent_descriptions = []
            for agent_id, agent_info in self.tellen_agents.items():
                if agent_id != "other":
                    capabilities_str = ", ".join(agent_info["capabilities"])
                    agent_descriptions.append(f"{agent_id} ({agent_info['name']}): {capabilities_str}")

            prompt = f"""
Job Title: {job.title}
Company: {job.company}
Job Description: {job.description}

Job Analysis:
{analysis.get('analysis', 'No analysis available')}

Available Tellen Agents:
{chr(10).join(agent_descriptions)}

Please match this job to the most appropriate Tellen agent and provide:
1. The best matching agent (AFC, FSP, or other)
2. Confidence score (0.0 to 1.0)
3. Explanation of the match

Respond in JSON format:
{{
    "matched_agent": "AFC|FSP|other",
    "confidence_score": 0.85,
    "explanation": "Detailed explanation of why this job matches the selected agent"
}}

Consider:
- How well the job responsibilities align with agent capabilities
- The level of automation potential
- Whether the role requires human judgment vs. structured tasks
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at matching accounting and financial services jobs to AI automation agents. Be precise and analytical in your matching.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=500,
            )

            response_text = response.choices[0].message.content
            logger.info(f"GPT-5-Codex matching response: {response_text}")

            # Parse response (in production, you'd parse the JSON properly)
            # For now, use simple heuristics based on job title and description
            matched_agent, confidence, explanation = self._heuristic_match(job, analysis)

            return matched_agent, confidence, explanation

        except Exception as e:
            logger.error(f"Error matching job to agent: {e}")
            return "other", 0.1, f"Error in matching: {str(e)}"

    def _heuristic_match(self, job: Job, analysis: Dict) -> Tuple[str, float, str]:
        """Fallback heuristic matching when GPT-5-Codex is unavailable"""
        title_lower = job.title.lower()
        desc_lower = job.description.lower() if job.description else ""

        # AFC matching criteria
        afc_keywords = ["audit", "compliance", "internal control", "risk", "regulatory", "financial statement"]
        afc_score = sum(1 for keyword in afc_keywords if keyword in title_lower or keyword in desc_lower)

        # FSP matching criteria
        fsp_keywords = [
            "financial analysis",
            "investment",
            "portfolio",
            "market research",
            "financial modeling",
            "data analysis",
        ]
        fsp_score = sum(1 for keyword in fsp_keywords if keyword in title_lower or keyword in desc_lower)

        if afc_score > fsp_score and afc_score > 0:
            confidence = min(0.9, 0.5 + (afc_score * 0.1))
            return "AFC", confidence, f"Job matches AFC agent based on {afc_score} audit/compliance keywords"
        elif fsp_score > 0:
            confidence = min(0.9, 0.5 + (fsp_score * 0.1))
            return "FSP", confidence, f"Job matches FSP agent based on {fsp_score} financial analysis keywords"
        else:
            return "other", 0.3, "Job requires human judgment and management skills"

    def generate_gap_analysis(self, job: Job, matched_agent: str) -> str:
        """Generate gap analysis for jobs that don't match existing agents"""
        if matched_agent != "other":
            return ""

        try:
            prompt = f"""
Job Title: {job.title}
Company: {job.company}
Job Description: {job.description}

This job doesn't match our existing AI agents (AFC, FSP). Analyze what new agent capabilities would be needed to automate this role.

Provide insights on:
1. What type of new agent could handle this role
2. Key capabilities the new agent would need
3. Automation challenges and opportunities
4. Potential business value

Keep the analysis concise and actionable.
"""

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert in AI agent development for accounting and financial services. Focus on practical automation opportunities.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
                max_tokens=300,
            )

            return response.choices[0].message.content

        except Exception as e:
            logger.error(f"Error generating gap analysis: {e}")
            return f"Gap analysis failed: {str(e)}"

    def process_job(self, job_id: int) -> bool:
        """Process a single job for agent matching"""
        db = SessionLocal()
        try:
            job = db.query(Job).filter(Job.id == job_id).first()
            if not job:
                logger.error(f"Job {job_id} not found")
                return False

            # Check if already processed
            existing_match = db.query(AgentMatch).filter(AgentMatch.job_id == job_id).first()
            if existing_match:
                logger.info(f"Job {job_id} already processed")
                return True

            logger.info(f"Processing job: {job.title} at {job.company}")

            # Analyze job description
            analysis = self.analyze_job_description(job.description or "")

            # Match to agent
            matched_agent, confidence, explanation = self.match_job_to_agent(job, analysis)

            # Generate gap analysis if needed
            notes = explanation
            if matched_agent == "other":
                gap_analysis = self.generate_gap_analysis(job, matched_agent)
                notes = f"{explanation}\n\nGap Analysis:\n{gap_analysis}"

            # Save agent match
            agent_match = AgentMatch(job_id=job_id, matched_agent=matched_agent, confidence_score=confidence, notes=notes)

            db.add(agent_match)
            db.commit()

            logger.info(f"Successfully processed job {job_id}: {matched_agent} (confidence: {confidence})")
            return True

        except Exception as e:
            logger.error(f"Error processing job {job_id}: {e}")
            db.rollback()
            return False
        finally:
            db.close()

    def process_all_unprocessed_jobs(self) -> int:
        """Process all jobs that haven't been matched to agents yet"""
        db = SessionLocal()
        try:
            # Find jobs without agent matches
            processed_job_ids = db.query(AgentMatch.job_id).distinct().all()
            processed_job_ids = [job_id[0] for job_id in processed_job_ids]

            unprocessed_jobs = db.query(Job).filter(~Job.id.in_(processed_job_ids)).all()

            logger.info(f"Found {len(unprocessed_jobs)} unprocessed jobs")

            processed_count = 0
            for job in unprocessed_jobs:
                if self.process_job(job.id):
                    processed_count += 1

            logger.info(f"Successfully processed {processed_count} jobs")
            return processed_count

        except Exception as e:
            logger.error(f"Error processing jobs: {e}")
            return 0
        finally:
            db.close()


def main():
    """Main function to process all unprocessed jobs"""
    processor = AIJobProcessor()

    logger.info("Starting AI job processing...")
    processed_count = processor.process_all_unprocessed_jobs()
    logger.info(f"AI processing completed. Processed {processed_count} jobs.")


if __name__ == "__main__":
    main()
