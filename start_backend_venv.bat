@echo off
echo ========================================
echo Starting Backend API Server (Virtual Env)
echo ========================================
echo.

cd backend
call venv\Scripts\activate.bat
python main.py
pause
