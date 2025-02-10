# Use a lightweight Python image
FROM python:3.9-slim

# Install PostgreSQL client and build tools
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
