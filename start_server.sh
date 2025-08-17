#!/bin/bash
# start_server.sh

echo "🚀 Starting PDF OCR FastAPI Server with uv..."

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies if not already
echo "📦 Installing dependencies with uv..."
uv pip install -r requirements.txt --quiet

# Run the FastAPI app using uv
echo "🔥 Starting FastAPI server on http://0.0.0.0:8000"
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload