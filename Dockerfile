FROM python:3.9-slim

WORKDIR /app

# Install system dependencies required for OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies and gunicorn
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (except start.sh which we'll copy separately)
COPY . .

# Make start.sh executable before copying to avoid permission issues
RUN chmod +x start.sh

# Create a non-root user to run the application
RUN useradd -m appuser

# Change ownership of the application directory to the non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE ${PORT:-8080}

# Command to run the application
CMD ["/app/start.sh"]
