@echo off
echo ========================================
echo Starting Camera Service (Virtual Env)
echo ========================================
echo.

cd camera_service
echo Current directory: %CD%
echo.
echo Starting with virtual environment Python...
echo.
venv\Scripts\python.exe attendance_service.py
pause
