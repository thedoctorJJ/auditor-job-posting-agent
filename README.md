# Auditor Job Posting Agent

An AI-powered application that continuously scans job boards for auditing and accounting job postings, extracts structured information, and analyzes which roles are best suited for automation by AI workforce agents.

## 🚀 Features

- **Automated Job Scraping**: Scrapes job postings from Indeed and other job boards
- **AI-Powered Analysis**: Uses GPT-4-Turbo to analyze job descriptions and match them to Tellen agents
- **Agent Matching**: Matches jobs to AFC (Accounting & Financial Compliance) and FSP (Financial Services Professional) agents
- **Outreach Generation**: Generates personalized outreach emails offering Tellen services at 20% of listed salary
- **Review Dashboard**: Human-in-the-loop approval system for outreach emails
- **REST API**: Complete FastAPI backend with comprehensive endpoints

## 🛠 Tech Stack

- **Backend**: Python 3.11+, FastAPI, SQLAlchemy
- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, shadcn/ui (planned)
- **Database**: SQLite (development) / Supabase (production)
- **AI**: OpenAI GPT-4-Turbo
- **Scraping**: BeautifulSoup, Selenium with mock data fallback
- **Email**: SendGrid (planned)
- **Deployment**: Docker, Google Cloud Run ready

## ⚡ Quick Start

### Prerequisites

- Python 3.11+
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

The API will be available at `http://localhost:8000` with interactive docs at `http://localhost:8000/docs`

## 📁 Project Structure

```
auditor-job-posting-agent/
├── backend/                    # FastAPI application
│   ├── models.py              # Database models (Job, AgentMatch, Outreach)
│   ├── database.py            # Database connection and session management
│   ├── ai_processor.py        # AI job processing with GPT-4-Turbo
│   ├── main.py               # FastAPI app with all endpoints
│   ├── init_db.py            # Database initialization script
│   └── test_*.py             # Test scripts
├── scraper/                   # Job scraping modules
│   ├── indeed_scraper.py     # Indeed scraper (with 403 fallback)
│   ├── mock_scraper.py       # Mock data generator for development
│   └── test_run.py           # Test script for 10 job postings
├── requirements/              # Python dependencies
│   ├── backend-requirements.txt
│   └── scraper-requirements.txt
├── frontend/                  # Next.js dashboard (planned)
├── docs/                      # Documentation
├── tests/                     # Test files
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
- `PUT /outreach/{id}/approve` - Approve outreach email
- `PUT /outreach/{id}/reject` - Reject outreach email

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

# Email Configuration (Optional - for future email functionality)
SENDGRID_API_KEY=your_sendgrid_api_key
FROM_EMAIL=your_email@domain.com
FROM_NAME=Your Name

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

3. **Test API endpoints**
   ```bash
   # Start the server
   cd backend && uvicorn main:app --reload
   
   # Test endpoints
   curl http://localhost:8000/jobs
   curl http://localhost:8000/agent-matches
   curl http://localhost:8000/stats
   ```

### Expected Results

- **10 test jobs** generated and saved to database
- **AI processing** matches jobs to AFC/FSP agents with confidence scores
- **API endpoints** return structured JSON data
- **Statistics** show job counts and agent distribution

## 🚀 Development Commands

```bash
# Set up everything
make setup

# Start development server
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
- [x] Docker configuration
- [x] CI/CD pipeline
- [x] Comprehensive documentation

### 🚧 In Progress
- [ ] Frontend dashboard (Next.js)
- [ ] Outreach email generation system
- [ ] SendGrid email integration

### 📋 Planned
- [ ] Production deployment to Google Cloud
- [ ] Advanced job board scraping
- [ ] Email template customization
- [ ] Analytics and reporting dashboard

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

- **v1.1**: Frontend dashboard with job management
- **v1.2**: Email outreach system with templates
- **v1.3**: Advanced analytics and reporting
- **v2.0**: Multi-job-board scraping and ML improvements

---

**Built with ❤️ by the Tellen team**