#!/bin/bash

# Start Web Application for AI Code Assistant
# This script starts both the backend and frontend servers

echo "================================"
echo "AI Code Assistant - Web Version"
echo "================================"
echo ""

# Check if ANTHROPIC_API_KEY is set
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Error: ANTHROPIC_API_KEY environment variable is not set"
    echo "Please set it with: export ANTHROPIC_API_KEY='your-key-here'"
    exit 1
fi

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "Error: uv is not installed"
    echo "Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "Starting backend server on port 8000..."
uv run api.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

echo "Installing frontend dependencies (if needed)..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi

echo "Starting frontend server on port 5173..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "================================"
echo "Servers are running!"
echo "================================"
echo "Backend:  http://localhost:8000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Trap Ctrl+C and call cleanup
trap cleanup INT

# Wait for both processes
wait
