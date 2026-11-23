#!/bin/bash
set -e

echo "=========================================================="
echo "🚀 Deploying OfficeMate 2.0 under 'officemate' brand"
echo "=========================================================="

IMAGE_NAME="officemate:latest"
CONTAINER_NAME="officemate-app"

if command -v docker &> /dev/null; then
    echo "1. Building Docker image: $IMAGE_NAME ..."
    docker build -t "$IMAGE_NAME" .

    echo "2. Stopping existing container if running..."
    docker stop "$CONTAINER_NAME" 2>/dev/null || true
    docker rm "$CONTAINER_NAME" 2>/dev/null || true

    echo "3. Starting container: $CONTAINER_NAME on ports 8501 & 5000..."
    docker run -d \
        --name "$CONTAINER_NAME" \
        -p 8501:8501 \
        -p 5000:5000 \
        -v officemate-data:/app/data \
        "$IMAGE_NAME"

    echo "✅ OfficeMate container deployed successfully!"
    echo "   Web App: http://localhost:8501"
    echo "   API:     http://localhost:5000"
else
    echo "⚠️ Docker not detected in this environment."
    echo "Deploying OfficeMate via native Python daemon launcher..."
    ./run_frontend.sh &
    ./run_backend.sh &
    echo "✅ OfficeMate services started natively in background!"
    echo "   Web App: http://localhost:8501"
    echo "   API:     http://localhost:5000"
fi
echo "=========================================================="
