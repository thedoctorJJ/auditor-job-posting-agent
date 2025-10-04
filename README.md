# Auditor Job Posting Agent

An AI-powered full-stack application that continuously scans job boards for auditing and accounting job postings, extracts structured information, and analyzes which roles are best suited for automation by AI workforce agents.

## 🚀 Features

- **Automated Job Scraping**: Scrapes job postings from Indeed and other job boards
- **AI-Powered Analysis**: Uses GPT-4-Turbo to analyze job descriptions and match them to Tellen agents
- **Agent Matching**: Matches jobs to AFC (Accounting & Financial Compliance) and FSP (Financial Services Professional) agents
- **Outreach Generation**: Generates personalized outreach emails offering Tellen services at 20% of listed salary
- **Review Dashboard**: Human-in-the-loop approval system for outreach emails
- **REST API**: Complete FastAPI backend with comprehensive endpoints
- **Modern Frontend**: Next.js dashboard with real-time statistics and management

## 🛠 Tech Stack

- **Backend**: Python 3.13+, FastAPI, SQLAlchemy
- **Frontend**: Next.js 15, TypeScript, Tailwind CSS
- **Database**: SQLite (development) / Supabase (production)
- **AI**: OpenAI GPT-4-Turbo
- **Scraping**: BeautifulSoup, Selenium with mock data fallback
- **Email**: SMTP integration with SendGrid support
- **Deployment**: Docker, Google Cloud Run ready

## ⚡ Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- OpenAI API key
- (Optional) SendGrid API key for email functionality
- (Optional) Supabase account for production database

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
   # Edit .env with your API keys (see Configuration section)
   ```

4. **Initialize the database**
   ```bash
   python backend/init_db.py
   ```

5. **Run a test scrape (10 jobs)**
   ```bash
   python scraper/test_run.py
   ```

6. **Process jobs with AI**
   ```bash
   python backend/ai_processor.py
   ```

7. **Start the API server**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

8. **Start the frontend (in a new terminal)**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`
The frontend dashboard will be available at `http://localhost:3000`

## 📁 Project Structure

```
auditor-job-posting-agent/
├── backend/                    # FastAPI application
│   ├── models.py              # Database models (Job, AgentMatch, Outreach)
│   ├── database.py            # Database connection and session management
│   ├── ai_processor.py        # AI job processing with GPT-4-Turbo
│   ├── email_service.py       # Email generation and sending
│   ├── main.py               # FastAPI app with all endpoints
│   └── init_db.py            # Database initialization script
├── frontend/                  # Next.js dashboard
│   ├── src/app/              # App router pages
│   ├── src/components/ui/    # Reusable UI components
│   └── src/lib/              # API client and utilities
├── scraper/                   # Job scraping modules
│   ├── indeed_scraper.py     # Indeed scraper (with 403 fallback)
│   ├── mock_scraper.py       # Mock data generator for development
│   └── test_run.py           # Test script for 10 job postings
├── requirements/              # Python dependencies
├── tests/                     # Test files
├── docs/                      # Documentation
├── .github/workflows/         # CI/CD pipeline
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Multi-service setup
├── Makefile                   # Development commands
└── README.md                  # This file
```

## 🔌 API Endpoints

### Jobs
- `GET /jobs` - List all job postings with pagination
- `GET /jobs/{id}` - Get specific job details
- `GET /jobs/{id}/matches` - Get agent matches for a job

### Agent Matches
- `GET /agent-matches` - List agent matches with filtering
- Filter by: `agent` (AFC/FSP/other), `min_confidence`

### Outreach
- `GET /outreach` - List outreach emails with status filtering
- `GET /outreach/{id}` - Get specific outreach email
- `POST /outreach/generate/{job_id}` - Generate outreach for specific job
- `POST /outreach/generate-all` - Generate outreach for all high-confidence jobs
- `PUT /outreach/{id}/approve` - Approve outreach email
- `PUT /outreach/{id}/reject` - Reject outreach email
- `POST /outreach/{id}/send` - Send approved outreach email

### Statistics
- `GET /stats` - Get system statistics (jobs, matches, outreach counts)

### Health
- `GET /` - Root endpoint with API info
- `GET /health` - Health check endpoint

## ⚙️ Configuration

### Required Environment Variables

```bash
# OpenAI Configuration (Required)
OPENAI_API_KEY=sk-proj-your-openai-api-key
OPENAI_MODEL=gpt-4-turbo

# Application Configuration (Required)
SECRET_KEY=your-secret-key-for-jwt-tokens
```

### Optional Environment Variables

```bash
# Database Configuration (Optional - uses SQLite if not set)
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# Email Configuration (Optional - for email functionality)
SENDGRID_API_KEY=your_sendgrid_api_key
FROM_EMAIL=your_email@domain.com
FROM_NAME=Your Name
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_USERNAME=your_email@gmail.com
EMAIL_PASSWORD=your_app_password

# Scraping Configuration (Optional)
SCRAPING_DELAY=2
MAX_RETRIES=3
USER_AGENT_ROTATION=true

# Development Configuration (Optional)
DEBUG=true
LOG_LEVEL=INFO
```

## 🧪 Testing

### Test the System

1. **Generate test data**
   ```bash
   python scraper/test_run.py
   ```

2. **Process with AI**
   ```bash
   python backend/ai_processor.py
   ```

3. **Generate outreach emails**
   ```bash
   python -c "
   import sys; sys.path.append('.')
   from backend.email_service import generate_outreach_for_all_high_confidence_jobs
   generate_outreach_for_all_high_confidence_jobs()
   "
   ```

4. **Test API endpoints**
   ```bash
   # Start the server
   cd backend && uvicorn main:app --reload
   
   # Test endpoints
   curl http://localhost:8000/jobs
   curl http://localhost:8000/agent-matches
   curl http://localhost:8000/stats
   ```

5. **Run automated tests**
   ```bash
   python -m pytest tests/ -v
   ```

### Expected Results

- **10 test jobs** generated and saved to database
- **AI processing** matches jobs to AFC/FSP agents with confidence scores
- **10 outreach emails** generated with personalized templates
- **API endpoints** return structured JSON data
- **Frontend dashboard** displays real-time statistics
- **All tests pass** (11/11 tests)

## 🚀 Development Commands

```bash
# Set up everything
make setup

# Start development servers
make dev

# Run tests
make test

# Initialize database
make init-db

# Test scraping
make test-scrape

# Process jobs with AI
make process-jobs

# Format code
make format

# Run linting
make lint
```

## 📊 Current Status

### ✅ Completed
- [x] Project structure and environment setup
- [x] Database schema with SQLite/Supabase support
- [x] Job scraping system with mock data fallback
- [x] AI-powered job processing with GPT-4-Turbo
- [x] Complete FastAPI backend with all endpoints
- [x] Outreach email generation system
- [x] Next.js frontend dashboard
- [x] Docker configuration
- [x] CI/CD pipeline
- [x] Comprehensive testing (11/11 tests passing)
- [x] Professional documentation

### 🚧 In Progress
- [ ] Production deployment to Google Cloud
- [ ] Advanced job board scraping
- [ ] Email template customization
- [ ] Analytics and reporting dashboard

### 📋 Planned
- [ ] Multi-job-board scraping
- [ ] Advanced AI matching algorithms
- [ ] Email campaign management
- [ ] Performance analytics
- [ ] User authentication and roles

## 🐳 Docker Support

### Build and Run
```bash
# Build image
docker build -t auditor-job-agent .

# Run container
docker run -p 8000:8000 --env-file .env auditor-job-agent
```

### Docker Compose
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and the `docs/` folder
- **Issues**: [GitHub Issues](https://github.com/thedoctorJJ/auditor-job-posting-agent/issues)
- **Discussions**: [GitHub Discussions](https://github.com/thedoctorJJ/auditor-job-posting-agent/discussions)

## 🎯 Roadmap

- **v1.1**: Production deployment and monitoring
- **v1.2**: Advanced analytics and reporting
- **v1.3**: Multi-job-board scraping
- **v2.0**: Machine learning improvements and automation

---

**Built with ❤️ by the Tellen team**

**Repository**: https://github.com/thedoctorJJ/auditor-job-posting-agent
**Status**: 🟢 **PRODUCTION READY**