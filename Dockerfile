FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
ENV DB_PATH=/app/data/parking.db

# Set work directory
WORKDIR /app

# Install system dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create volume mount point for persistent database
RUN mkdir -p /app/data

# Copy project files
COPY . .

# Expose container application port
EXPOSE 5000

# Run Flask application
CMD ["python", "app.py"]
