@echo off
curl.exe --silent --fail http://127.0.0.1:8000/health >nul 2>&1
if %errorlevel%==0 (
    echo NEELASTACK API is already running on http://127.0.0.1:8000
    exit /b 0
)
python -m uvicorn apps.api.main:app --reload --port 8000
