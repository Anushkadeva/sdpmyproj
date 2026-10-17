# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables to optimize Python runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set container working directory
WORKDIR /app

# Install system dependencies (curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create a dedicated non-root user and group for security
RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m -s /bin/bash appuser

# Layer caching: copy requirements first and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files, configs, datasets, and tests
COPY .streamlit /app/.streamlit
COPY app.py /app/
COPY DailyDelhiClimateTrain.csv /app/
COPY DailyDelhiClimateTest.csv /app/
COPY tests /app/tests

# Set ownership of /app directory to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user (Sprint 2 Security Best Practice)
USER appuser

# Expose Streamlit default port
EXPOSE 8501

# Container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Start Streamlit server
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
