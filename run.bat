@echo off
cd /d "%~dp0"

if not exist "venv\Scripts\python.exe" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create venv. Is Python 3.10+ installed?
        pause
        exit /b 1
    )
)

echo Installing dependencies...
venv\Scripts\python.exe -m pip install -q -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

set PORT=8000
netstat -ano | findstr ":%PORT% " | findstr LISTENING >nul 2>&1
if not errorlevel 1 set PORT=8080

echo.
echo GameNight API starting at http://127.0.0.1:%PORT%
echo   API docs:  http://127.0.0.1:%PORT%/docs
echo   Health:    http://127.0.0.1:%PORT%/api/health
echo Press Ctrl+C to stop.
echo.

start "" "http://127.0.0.1:%PORT%/docs"
venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port %PORT%

pause
