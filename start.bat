@echo off
echo ===================================================
echo   AI Summarizer Pro V2 - Launching Dev Environment
echo ===================================================
echo.
echo Cleaning Vite Cache...
if exist node_modules\.vite (rmdir /s /q node_modules\.vite)
echo Starting Vite Dev Server...
npm run dev
pause
