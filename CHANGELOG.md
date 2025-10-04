# Changelog

All notable changes to the Auditor Job Posting Agent project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup with FastAPI backend
- SQLite database with Job, AgentMatch, and Outreach models
- Mock job scraper for development and testing
- AI-powered job processing with GPT-4-Turbo
- Agent matching system (AFC and FSP agents)
- Basic FastAPI endpoints for jobs, matches, and outreach
- Docker configuration for containerization
- GitHub Actions CI/CD pipeline
- Comprehensive documentation and README

### Changed
- Updated from GPT-5-Codex to GPT-4-Turbo (GPT-5-Codex not available)

### Fixed
- Resolved Python 3.13 compatibility issues
- Fixed module import paths for proper package structure
- Corrected database file paths for consistent SQLite usage

## [1.0.0] - 2025-01-04

### Added
- Initial release
- Core job scraping functionality
- AI-powered job analysis and agent matching
- REST API with FastAPI
- Database schema and models
- Docker support
- Basic documentation

### Technical Details
- **Backend**: Python 3.11+, FastAPI, SQLAlchemy
- **Database**: SQLite (development), Supabase (production)
- **AI**: OpenAI GPT-4-Turbo
- **Scraping**: BeautifulSoup, Selenium with mock data fallback
- **Deployment**: Docker, Google Cloud Run ready
