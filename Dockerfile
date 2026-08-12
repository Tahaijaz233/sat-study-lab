# Dockerfile for SAT Study Lab - FastAPI + PostgreSQL app
# Optimized for Fly.io deployment

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies for psycopg2 (PostgreSQL)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories for static files and templates
RUN mkdir -p /app/app/static /app/app/templates

# Expose port (Fly.io uses PORT env var, defaulting to 8080)
ENV PORT=8080
EXPOSE 8080

# Run the application
# Use uvicorn with the PORT environment variable
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
