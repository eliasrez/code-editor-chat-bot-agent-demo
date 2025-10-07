# Quick Start Guide - Web UI

Get the web interface up and running in 5 minutes!

## Step 1: Prerequisites

Make sure you have:
- Python 3.12+ with `uv` installed
- Node.js 16+ installed
- An Anthropic API key

### Install uv (if not already installed)

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Install Node.js (if not already installed)

Download from: https://nodejs.org/

## Step 2: Set API Key

**Linux/macOS:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

**Windows:**
```cmd
set ANTHROPIC_API_KEY=your-api-key-here
```

## Step 3: Run the Application

### Option A: Use the start script (Recommended)

**Linux/macOS:**
```bash
chmod +x start-web.sh
./start-web.sh
```

**Windows:**
```cmd
start-web.bat
```

### Option B: Manual start

**Terminal 1 - Backend:**
```bash
uv run api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm install  # Only needed first time
npm run dev
```

## Step 4: Open in Browser

Navigate to: **http://localhost:5173**

## What You'll See

1. **Left Sidebar**: File explorer showing your project files
2. **Right Panel**: Split view with chat and file viewer
3. **Chat Interface**: Talk to the AI assistant

## Try These Commands

In the chat, try:
- "List all files in the current directory"
- "Show me the contents of main.py"
- "Create a file called hello.py with a simple hello world function"
- "Explain what the AIAgent class does"

## Troubleshooting

### Port already in use?

**Backend (8000):**
Edit `api.py` and change the port at the bottom:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed from 8000
```

**Frontend (5173):**
Edit `frontend/vite.config.js`:
```javascript
server: {
  port: 5174,  // Changed from 5173
  ...
}
```

### Can't connect to backend?

Check that:
1. Backend is running (you should see "Application startup complete")
2. No firewall blocking localhost
3. CORS settings in `api.py` match your frontend port

### Frontend won't start?

Try:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

## Next Steps

- Read `WEB_APP_README.md` for full documentation
- Customize the theme in CSS files
- Add new features to the AI agent

## Getting Help

Check the logs:
- Backend errors: Look at terminal running `api.py`
- Frontend errors: Check browser console (F12)
- Agent actions: Check `agent.log` file

Enjoy your AI Code Assistant!
