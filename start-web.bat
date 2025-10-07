@echo off
REM Start Web Application for AI Code Assistant (Windows)

echo ================================
echo AI Code Assistant - Web Version
echo ================================
echo.

REM Check if ANTHROPIC_API_KEY is set
if "%ANTHROPIC_API_KEY%"=="" (
    echo Error: ANTHROPIC_API_KEY environment variable is not set
    echo Please set it with: set ANTHROPIC_API_KEY=your-key-here
    exit /b 1
)

echo Starting backend server on port 8000...
start "AI Agent Backend" uv run api.py

timeout /t 3 /nobreak >nul

echo Installing frontend dependencies if needed...
cd frontend
if not exist "node_modules" (
    call npm install
)

echo Starting frontend server on port 5173...
start "AI Agent Frontend" npm run dev

echo.
echo ================================
echo Servers are running!
echo ================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Close both terminal windows to stop the servers
echo.

pause
