#!/bin/bash

# Script to build and run the OCR KTP API Docker container

set -e

echo "=== OCR KTP API Docker Helper ==="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Warning: Docker Compose is not installed. Using Docker commands instead."
    USE_COMPOSE=false
else
    USE_COMPOSE=true
fi

# Check for Google Cloud credentials
if [ -z "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
    echo "Warning: GOOGLE_APPLICATION_CREDENTIALS environment variable is not set."
    echo "The OCR functionality requires Google Cloud Vision API credentials."
    echo "You can set it with: export GOOGLE_APPLICATION_CREDENTIALS=\"path/to/your-credentials.json\""
    echo ""
    
    # Check if credentials.json exists in the current directory
    if [ -f "./credentials.json" ]; then
        echo "Found credentials.json in the current directory. This will be used by default."
    else
        echo "No credentials.json found in the current directory."
        echo "The application will start but OCR functionality will not work without credentials."
    fi
    echo ""
fi

# Function to build and run with Docker Compose
run_with_compose() {
    echo "Building and starting container with Docker Compose..."
    docker-compose up --build -d
    echo "Container started. API is available at http://localhost:5001"
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
}

# Function to build and run with Docker commands
run_with_docker() {
    echo "Building Docker image..."
    docker build -t ocr-ktp-api .
    
    echo "Starting container..."
    CREDENTIALS_MOUNT=""
    if [ -n "$GOOGLE_APPLICATION_CREDENTIALS" ]; then
        CREDENTIALS_MOUNT="-v $GOOGLE_APPLICATION_CREDENTIALS:/tmp/credentials.json:ro -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/credentials.json"
    elif [ -f "./credentials.json" ]; then
        CREDENTIALS_MOUNT="-v $(pwd)/credentials.json:/tmp/credentials.json:ro -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/credentials.json"
    fi
    
    docker run -d --name ocr-ktp-api -p 5001:5001 $CREDENTIALS_MOUNT ocr-ktp-api
    echo "Container started. API is available at http://localhost:5001"
    echo "To view logs: docker logs -f ocr-ktp-api"
    echo "To stop: docker stop ocr-ktp-api && docker rm ocr-ktp-api"
}

# Main execution
if [ "$USE_COMPOSE" = true ]; then
    run_with_compose
else
    run_with_docker
fi

echo ""
echo "=== Done ==="
