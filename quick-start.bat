@echo off
REM Quick Start Script for AI Summarizer Pro

cls
echo.
echo =========================================================
echo     AI SUMMARIZER PRO - QUICK START
echo =========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.13+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 16+ from https://nodejs.org
    pause
    exit /b 1
)

echo [OK] Python found: 
python --version

echo [OK] Node.js found: 
node --version

echo.
echo =========================================================
echo     Starting Application Setup
echo =========================================================
echo.

REM Create virtual environment if not exists
if not exist ".venv" (
    echo [*] Creating Python virtual environment...
    python -m venv .venv
    echo [OK] Virtual environment created
)

REM Activate virtual environment
echo [*] Activating Python virtual environment...
call .venv\Scripts\activate.bat

REM Install backend dependencies
echo.
echo [*] Installing backend dependencies...
cd backend
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install backend dependencies
    pause
    exit /b 1
)
echo [OK] Backend dependencies installed
cd ..

REM Install frontend dependencies
echo.
echo [*] Installing frontend dependencies...
cd frontend
npm install --legacy-peer-deps --quiet 2>nul
if errorlevel 1 (
    echo [WARNING] Some npm warnings detected, but continuing...
)
echo [OK] Frontend dependencies installed
cd ..

echo.
echo =========================================================
echo     Setup Complete!
echo =========================================================
echo.
echo Your application is ready to run. Choose how to start:
echo.
echo [1] Start Web Version (npm start)
echo [2] Start Desktop App (Electron)
echo [3] Manual - Backend Server Only
echo [4] Manual - Frontend Server Only
echo [5] Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    cd frontend
    npm start
) else if "%choice%"=="2" (
    cd frontend
    npm run electron-dev
) else if "%choice%"=="3" (
    cd backend
    python -m uvicorn main:app --reload --port 8000
) else if "%choice%"=="4" (
    cd frontend
    npm start
) else if "%choice%"=="5" (
    exit /b 0
) else (
    echo Invalid choice. Exiting.
    exit /b 1
)

pause