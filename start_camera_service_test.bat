@echo off
echo ========================================
echo Starting Camera Service - TEST MODE
echo ========================================
echo.
echo This will test API connectivity without camera
echo.

cd camera_service
call venv\Scripts\activate.bat
python attendance_service_test.py
pause
