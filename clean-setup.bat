@echo off
REM Clean install script for AI Summarizer Pro
echo ========================================
echo AI Summarizer Pro - Clean Setup
echo ========================================

REM Kill any running node processes
taskkill /IM node.exe /F 2>nul
taskkill /IM electron.exe /F 2>nul

timeout /t 2 /nobreak

REM Remove node_modules in frontend
echo Removing old node_modules...
cd frontend
if exist node_modules (
    rmdir /s /q node_modules 2>nul
)

REM Clear npm cache
echo Clearing npm cache...
npm cache clean --force

REM Clean package-lock.json
if exist package-lock.json (
    del package-lock.json
)

REM Install fresh dependencies
echo Installing dependencies...
npm install --legacy-peer-deps

REM Install backend dependencies
cd ..\backend
echo Installing backend dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo   Windows: Run start.bat from project root
echo   Or run npm run electron-dev in frontend folder
echo.
pause