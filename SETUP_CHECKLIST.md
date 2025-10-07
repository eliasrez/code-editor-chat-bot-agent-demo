# Setup Checklist for Web UI

Follow this checklist to get your AI Code Assistant Web UI up and running!

## Prerequisites Check

### Required Software

- [ ] **Python 3.12 or higher** installed
  ```bash
  python --version  # or python3 --version
  ```

- [ ] **uv package manager** installed
  ```bash
  uv --version
  ```
  If not installed:
  - Linux/macOS: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`

- [ ] **Node.js 16 or higher** installed
  ```bash
  node --version
  npm --version
  ```
  If not installed: Download from https://nodejs.org/

- [ ] **Anthropic API Key** obtained
  Get one at: https://console.anthropic.com/settings/keys

## Environment Setup

- [ ] **Set API Key**
  
  Linux/macOS:
  ```bash
  export ANTHROPIC_API_KEY="your-api-key-here"
  # Add to ~/.bashrc or ~/.zshrc for persistence
  ```
  
  Windows (Command Prompt):
  ```cmd
  set ANTHROPIC_API_KEY=your-api-key-here
  ```
  
  Windows (PowerShell):
  ```powershell
  $env:ANTHROPIC_API_KEY="your-api-key-here"
  ```

- [ ] **Verify API key is set**
  ```bash
  echo $ANTHROPIC_API_KEY  # Linux/macOS
  echo %ANTHROPIC_API_KEY%  # Windows CMD
  echo $env:ANTHROPIC_API_KEY  # Windows PowerShell
  ```

## Installation

### Option A: Quick Start (Recommended)

- [ ] **Make start script executable** (Linux/macOS only)
  ```bash
  chmod +x start-web.sh
  ```

- [ ] **Run the start script**
  
  Linux/macOS:
  ```bash
  ./start-web.sh
  ```
  
  Windows:
  ```cmd
  start-web.bat
  ```

- [ ] **Wait for both servers to start** (about 10-15 seconds)

### Option B: Manual Start

#### Backend

- [ ] **Test backend can start**
  ```bash
  uv run api.py
  ```

- [ ] **Verify backend is running**
  - Should see: "Application startup complete"
  - Should be accessible at: http://localhost:8000
  - Press Ctrl+C to stop

#### Frontend

- [ ] **Navigate to frontend directory**
  ```bash
  cd frontend
  ```

- [ ] **Install dependencies** (first time only)
  ```bash
  npm install
  ```
  This may take 1-2 minutes

- [ ] **Start development server**
  ```bash
  npm run dev
  ```

- [ ] **Verify frontend is running**
  - Should see: "Local: http://localhost:5173"
  - Browser may open automatically

## Verification

- [ ] **Open browser** to http://localhost:5173

- [ ] **Check interface loads**
  - See purple header with "AI Code Assistant"
  - See "Explorer" sidebar on left
  - See "Chat" panel on right

- [ ] **Test file explorer**
  - Click on a file in the explorer
  - File viewer should appear
  - Code should be syntax highlighted

- [ ] **Test chat functionality**
  - Type: "List all files in the current directory"
  - Press Send or hit Enter
  - Should see AI response

- [ ] **Test file operations**
  - Type: "Show me the contents of main.py"
  - Should see the file contents in the response

## Troubleshooting

### Backend Issues

- [ ] **Port 8000 already in use?**
  - Find and stop the process using port 8000
  - Or edit `api.py` to use a different port

- [ ] **API key error?**
  - Verify `ANTHROPIC_API_KEY` is set correctly
  - Try setting it in the current terminal session

- [ ] **Module not found errors?**
  - `uv` should handle dependencies automatically
  - Try: `uv pip install anthropic fastapi uvicorn pydantic`

### Frontend Issues

- [ ] **Port 5173 already in use?**
  - Edit `frontend/vite.config.js` to use different port
  - Or stop the process using port 5173

- [ ] **npm install fails?**
  - Try: `npm cache clean --force`
  - Delete `node_modules` and `package-lock.json`
  - Run `npm install` again

- [ ] **Cannot connect to backend?**
  - Verify backend is running on port 8000
  - Check browser console (F12) for errors
  - Verify CORS settings in `api.py`

### Common Issues

- [ ] **Blank page?**
  - Check browser console (F12) for errors
  - Verify both servers are running
  - Try hard refresh (Ctrl+Shift+R or Cmd+Shift+R)

- [ ] **Chat not working?**
  - Check network tab in browser DevTools
  - Verify backend is responding at http://localhost:8000
  - Check backend terminal for errors

- [ ] **Files not showing?**
  - Verify you're in the correct directory
  - Check file permissions
  - Look at backend terminal for error messages

## Post-Setup

### Verify Everything Works

- [ ] **Create a test file**
  - In chat: "Create a file called test.txt with the text 'Hello World'"
  - Check that file appears in explorer
  - Click to view it

- [ ] **Edit a file**
  - "Add 'This is a test' to test.txt"
  - Verify the change

- [ ] **Read a file**
  - "Show me test.txt"
  - Should see the contents

### Optional Enhancements

- [ ] **Add API key to shell profile** (for persistence)
  
  Linux/macOS (~/.bashrc or ~/.zshrc):
  ```bash
  export ANTHROPIC_API_KEY="your-api-key-here"
  ```
  
  Windows (System Environment Variables):
  1. Search "Environment Variables"
  2. Add new variable: ANTHROPIC_API_KEY
  3. Restart terminal

- [ ] **Create desktop shortcut** to start script

- [ ] **Bookmark** http://localhost:5173 in browser

## Next Steps

- [ ] **Read WEB_APP_README.md** for full documentation

- [ ] **Review ARCHITECTURE.md** to understand how it works

- [ ] **Check CLI_VS_WEB.md** to see differences

- [ ] **Explore UI_PREVIEW.md** for interface details

- [ ] **Start using it!** Try different commands and explore features

## Success Criteria

You know everything is working correctly when:

✅ Backend shows "Application startup complete"
✅ Frontend opens in browser automatically
✅ File explorer shows your project files
✅ Clicking a file displays its contents with syntax highlighting
✅ Chat responds to your messages
✅ AI can read and modify files
✅ No error messages in either terminal
✅ No console errors in browser (F12)

## Getting Help

If you're stuck:

1. **Check the logs**
   - Backend: Terminal running `api.py`
   - Frontend: Terminal running `npm run dev`
   - Agent: `agent.log` file
   - Browser: Console (F12)

2. **Review documentation**
   - QUICKSTART.md - Basic setup
   - WEB_APP_README.md - Detailed docs
   - ARCHITECTURE.md - Technical details

3. **Common solutions**
   - Restart both servers
   - Check API key is set
   - Verify ports are available
   - Clear browser cache
   - Check file permissions

## Maintenance

### Regular Tasks

- [ ] **Clear old logs** occasionally
  ```bash
  rm agent.log
  ```

- [ ] **Update dependencies** periodically
  ```bash
  # Backend (via uv)
  uv pip install --upgrade anthropic fastapi uvicorn
  
  # Frontend
  cd frontend
  npm update
  ```

### Before Sharing

- [ ] Remove or reset `agent.log`
- [ ] Clear any test files created
- [ ] Verify `.gitignore` is working
- [ ] Test in a clean environment

## Completion

- [ ] **All checks passed?** You're ready to use your Web UI!

- [ ] **Having issues?** Review the troubleshooting section

- [ ] **Everything working?** Enjoy your AI Code Assistant!

---

**Time to Complete**: 5-10 minutes
**Difficulty**: Easy to Moderate
**Support**: Check documentation files for help

Happy coding! 🚀
