@echo off
echo ========================================
echo Starting Camera Service (Virtual Env)
echo ========================================
echo.

cd camera_service
call venv\Scripts\activate.bat
python attendance_service.py
pause
