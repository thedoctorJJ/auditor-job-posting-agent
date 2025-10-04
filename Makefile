# Auditor Job Posting Agent Makefile

.PHONY: help setup dev test lint clean install-backend install-frontend

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Set up the entire project
	@echo "Setting up Auditor Job Posting Agent..."
	@$(MAKE) install-backend
	@$(MAKE) install-frontend
	@echo "Setup complete! Run 'make dev' to start development servers."

install-backend: ## Install Python dependencies
	@echo "Installing Python dependencies..."
	python -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements/backend-requirements.txt
	. venv/bin/activate && pip install -r requirements/scraper-requirements.txt

install-frontend: ## Install Node.js dependencies
	@echo "Installing Node.js dependencies..."
	cd frontend && npm install

dev: ## Start development servers
	@echo "Starting development servers..."
	. venv/bin/activate && uvicorn backend.main:app --reload --port 8000 &
	cd frontend && npm run dev

test: ## Run tests
	@echo "Running tests..."
	. venv/bin/activate && pytest tests/ -v

lint: ## Run linting
	@echo "Running linting..."
	. venv/bin/activate && flake8 backend/ scraper/
	. venv/bin/activate && black backend/ scraper/

format: ## Format code
	@echo "Formatting code..."
	. venv/bin/activate && black backend/ scraper/

clean: ## Clean up generated files
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf htmlcov/

init-db: ## Initialize database
	@echo "Initializing database..."
	. venv/bin/activate && python backend/init_db.py

test-scrape: ## Run test scraping
	@echo "Running test scrape..."
	. venv/bin/activate && python scraper/test_run.py

process-jobs: ## Process jobs with AI
	@echo "Processing jobs with AI..."
	. venv/bin/activate && python backend/ai_processor.py

docker-build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -t auditor-job-agent .

docker-run: ## Run Docker container
	@echo "Running Docker container..."
	docker run -p 8000:8000 --env-file .env auditor-job-agent
