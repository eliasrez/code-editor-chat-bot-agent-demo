# Docker Setup for AI Code Assistant

This document explains how to run the AI Code Assistant using Docker with both backend API and frontend application.

## Prerequisites

- Docker installed (version 20.10 or higher)
- Docker Compose installed (version 2.0 or higher)
- Anthropic API key

## Quick Start

1. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Anthropic API key:
   ```
   ANTHROPIC_API_KEY=your_actual_api_key_here
   ```

3. Build and start all services:
   ```bash
   docker-compose up --build
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Available Services

### Full Stack (API + Frontend)

Start both backend and frontend:
```bash
docker-compose up --build
```

This will start:
- API service on port 8000
- Frontend service on port 3000

### Development Mode

For frontend development with hot-reload:
```bash
docker-compose -f docker-compose.dev.yml up
```

This mode:
- Mounts frontend source code for instant updates
- Runs Vite dev server with HMR (Hot Module Replacement)
- Automatically installs npm dependencies

### API Service Only

Run just the backend API:
```bash
docker-compose up api
```

Access points:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend Service Only

Run just the frontend:
```bash
docker-compose up frontend
```

Access at http://localhost:3000

### CLI Service (optional)

To run the interactive command-line interface:
```bash
docker-compose --profile cli up cli
```

Or run interactively:
```bash
docker-compose run --rm cli python main.py
```

## Common Commands

### Start all services in detached mode:
```bash
docker-compose up -d
```

### View logs:
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f api
docker-compose logs -f frontend
```

### Stop services:
```bash
docker-compose down
```

### Rebuild after code changes:
```bash
docker-compose up --build
```

### Run a one-off command:
```bash
docker-compose run --rm api python main.py
```

### Access container shell:
```bash
# Backend
docker-compose exec api bash

# Frontend (dev mode)
docker-compose -f docker-compose.dev.yml exec frontend sh
```

### Clean up everything (including volumes):
```bash
docker-compose down -v
```

## Production Deployment

For production, the default docker-compose.yml is configured for production use:

```bash
docker-compose up -d --build
```

This will:
- Build the frontend as static files
- Serve frontend through nginx
- Run API with production settings
- Enable restart policies

### Production Optimizations

Create `docker-compose.prod.yml` for additional production settings:

```yaml
version: '3.8'

services:
  api:
    command: uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
    volumes:
      - ./logs:/app/logs
    
  frontend:
    environment:
      - VITE_API_URL=https://your-api-domain.com
```

Then run:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

## Environment Variables

### Backend (API)
- `ANTHROPIC_API_KEY` - Your Anthropic API key (required)

### Frontend
- `VITE_API_URL` - Backend API URL (default: http://localhost:8000)

## Volumes

- `./logs` - Persistent logs directory (backend)
- `.:/app` - Application code (mounted for development hot-reload)
- `/app/node_modules` - Node modules cache (dev mode)

## Port Configuration

Default ports:
- Frontend: 3000
- API: 8000

To change ports, modify the docker-compose.yml:
```yaml
services:
  frontend:
    ports:
      - "8080:80"  # Map to port 8080 instead
  
  api:
    ports:
      - "8001:8000"  # Map to port 8001 instead
```

## Architecture

### Production Build (docker-compose.yml)
```
┌─────────────────┐
│   Frontend      │  Port 3000
│   (nginx)       │  Static files
└────────┬────────┘
         │
    ┌────▼─────┐
    │ Network  │
    └────┬─────┘
         │
┌────────▼────────┐
│   API           │  Port 8000
│   (FastAPI)     │  Python backend
└─────────────────┘
```

### Development Build (docker-compose.dev.yml)
```
┌─────────────────┐
│   Frontend      │  Port 3000
│   (Vite dev)    │  Hot reload
└────────┬────────┘
         │
    ┌────▼─────┐
    │ Network  │
    └────┬─────┘
         │
┌────────▼────────┐
│   API           │  Port 8000
│   (FastAPI)     │  Hot reload
└─────────────────┘
```

## Troubleshooting

### Frontend can't connect to API

Check the VITE_API_URL environment variable:
```bash
docker-compose logs frontend
```

Ensure it points to the correct API URL.

### Port already in use

Change the port mapping in docker-compose.yml or stop the conflicting service:
```bash
# Find what's using the port
lsof -i :3000
lsof -i :8000
```

### Frontend not updating in dev mode

Make sure you're using the dev compose file:
```bash
docker-compose -f docker-compose.dev.yml up
```

### Build cache issues

Clear Docker cache:
```bash
docker-compose down
docker system prune -a
docker-compose up --build
```

## Notes

- The production frontend is served via nginx with optimized caching and compression
- Development mode provides hot-reload for both frontend and backend
- The CLI service is optional and only runs when explicitly requested
- All services are connected via a dedicated Docker network
- Frontend build uses multi-stage Docker build for smaller image size
- API includes CORS configuration for frontend communication
