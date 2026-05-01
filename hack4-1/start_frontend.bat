@echo off
chcp 65001 >nul
echo =============================================
echo   AI Travel Planner - Frontend
echo =============================================
cd /d "%~dp0frontend"

echo Installing npm packages...
npm install

echo.
echo Starting React app on http://localhost:3000
npm run dev
pause
