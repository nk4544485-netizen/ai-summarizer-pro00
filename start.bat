@echo off
echo Starting AI Summarizer Pro...

echo Starting Backend Server...
start cmd /k "cd backend && ..\.venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"

echo Starting Frontend Server...
start cmd /k "cd frontend && IF NOT EXIST node_modules\ (echo Installing dependencies... && npm install) && npm start"

echo Both servers are starting up!
