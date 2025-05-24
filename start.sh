#!/bin/bash

# Set default port if not provided
PORT=${PORT:-8080}

# Print startup message
echo "Starting OCR KTP API on port $PORT"

# Run the application with Gunicorn for production deployment
exec gunicorn --bind 0.0.0.0:$PORT app:app --workers 4
