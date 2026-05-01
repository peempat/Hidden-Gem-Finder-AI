@echo off
chcp 65001 >nul
echo =============================================
echo   AI Travel Planner - Backend
echo =============================================
cd /d "%~dp0backend"

if not exist ".env" (
    copy .env.example .env
    echo Created .env file - please add your GROQ_API_KEY!
    pause
)

echo Installing Python dependencies...
python -m pip install -r requirements.txt

echo.
echo Starting FastAPI server on http://localhost:8000
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
pause
