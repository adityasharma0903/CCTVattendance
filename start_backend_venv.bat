@echo off
echo ========================================
echo Starting Backend API Server (Virtual Env)
echo ========================================
echo.

cd backend

REM Use EXACT python from .venv (no activate needed)
"..\.venv\Scripts\python.exe" main.py

pause
