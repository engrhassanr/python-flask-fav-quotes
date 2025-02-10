# Use a lightweight Python image
FROM python:3.9-slim

# Install PostgreSQL client and build tools
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# Run Gunicorn server
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--workers", "4", "app:app"]

