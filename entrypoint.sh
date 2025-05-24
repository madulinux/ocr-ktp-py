#!/bin/bash

# Set default port if not provided
PORT=${PORT:-8080}

# Print startup message
echo "Starting OCR KTP API on port $PORT"

# Run the application with Python directly
# This is more reliable for environment variable handling
exec python app.py
