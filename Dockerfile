# Multi-stage build for the Auditor Job Posting Agent

# Backend stage
FROM python:3.11-slim as backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements/backend-requirements.txt requirements/scraper-requirements.txt ./
RUN pip install --no-cache-dir -r backend-requirements.txt -r scraper-requirements.txt

# Copy backend code
COPY backend/ ./backend/
COPY scraper/ ./scraper/

# Frontend stage
FROM node:18-alpine as frontend

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy frontend code
COPY frontend/ ./

# Build the application
RUN npm run build

# Production stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies
COPY requirements/backend-requirements.txt requirements/scraper-requirements.txt ./
RUN pip install --no-cache-dir -r backend-requirements.txt -r scraper-requirements.txt

# Copy application code
COPY backend/ ./backend/
COPY scraper/ ./scraper/
COPY --from=frontend /app/.next ./frontend/.next
COPY --from=frontend /app/public ./frontend/public
COPY --from=frontend /app/package*.json ./frontend/

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose ports
EXPOSE 8000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start command
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
