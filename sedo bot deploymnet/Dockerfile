# Production Dockerfile for SEDO MARTIAL ART Telegram Bot System
FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8080

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . /app/

# Create non-root user for security and grant permissions
RUN useradd -u 10001 -m -s /bin/sh appuser && \
    mkdir -p /app/uploads /app/data && \
    chown -R appuser:appuser /app

USER appuser

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

EXPOSE 8080

# Run bot in unbuffered mode
CMD ["python", "-u", "main.py"]
