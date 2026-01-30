@echo off
REM Start Camera Service
cd camera_service
echo.
echo ========================================
echo Starting Camera Service...
echo ========================================
echo.
python attendance_service.py
pause
