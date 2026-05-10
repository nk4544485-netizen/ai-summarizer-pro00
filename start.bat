@echo off
echo Starting MindMap AI Pro...

:: Start Backend
start cmd /k "echo Starting FastAPI Backend... && python -m uvicorn backend.main:app --reload --port 8000"

:: Start Frontend
start cmd /k "echo Starting React Frontend... && npm run dev"

echo Backend and Frontend are starting.
echo Chrome will open automatically if configured, or visit http://localhost:5173
timeout /t 5
start chrome http://localhost:5173
