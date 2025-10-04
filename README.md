# Auditor Job Posting Agent

An AI-powered application that continuously scans job boards for auditing and accounting job postings, extracts structured information, and analyzes which roles are best suited for automation by AI workforce agents.

## Features

- **Automated Job Scraping**: Scrapes job postings from Indeed and other job boards
- **AI-Powered Analysis**: Uses GPT-4-Turbo to analyze job descriptions and match them to Tellen agents
- **Agent Matching**: Matches jobs to AFC (Accounting & Financial Compliance) and FSP (Financial Services Professional) agents
- **Outreach Generation**: Generates personalized outreach emails offering Tellen services at 20% of listed salary
- **Review Dashboard**: Human-in-the-loop approval system for outreach emails

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, shadcn/ui
- **Database**: SQLite (development) / Supabase (production)
- **AI**: OpenAI GPT-4-Turbo
- **Scraping**: BeautifulSoup, Selenium
- **Email**: SendGrid
- **Deployment**: Google Cloud Run

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key
- SendGrid API key (optional)
- Supabase account (optional)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/thedoctorJJ/auditor-job-posting-agent.git
   cd auditor-job-posting-agent
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements/backend-requirements.txt
   pip install -r requirements/scraper-requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your API keys
   ```

4. **Initialize the database**
   ```bash
   python backend/init_db.py
   ```

5. **Run a test scrape**
   ```bash
   python scraper/test_run.py
   ```

6. **Process jobs with AI**
   ```bash
   python backend/ai_processor.py
   ```

### Development

**Backend API**
```bash
cd backend
uvicorn main:app --reload
```

**Frontend Dashboard**
```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
auditor-job-posting-agent/
├── backend/                 # FastAPI application
│   ├── models.py           # Database models
│   ├── database.py         # Database connection
│   ├── ai_processor.py     # AI job processing
│   └── main.py            # FastAPI app
├── frontend/               # Next.js dashboard
├── scraper/                # Job scraping modules
│   ├── indeed_scraper.py   # Indeed scraper
│   └── mock_scraper.py     # Mock data generator
├── requirements/           # Python dependencies
├── docs/                   # Documentation
└── tests/                  # Test files
```

## API Endpoints

- `GET /jobs` - List all job postings
- `GET /jobs/{id}` - Get specific job
- `GET /agent-matches` - List agent matches
- `POST /outreach` - Create outreach email
- `PUT /outreach/{id}/approve` - Approve outreach email

## Configuration

### Environment Variables

```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4-turbo

# Database Configuration
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key

# Email Configuration
SENDGRID_API_KEY=your_sendgrid_key
FROM_EMAIL=your_email@domain.com

# Application Configuration
SECRET_KEY=your_secret_key
```

## Deployment

### Google Cloud Run

1. **Build and push Docker image**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/auditor-job-agent
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy --image gcr.io/PROJECT_ID/auditor-job-agent
   ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For questions or support, please open an issue on GitHub or contact the development team.
