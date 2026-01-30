@echo off
REM Install all dependencies
echo.
echo ========================================
echo Installing Dependencies...
echo ========================================
echo.

echo.
echo Installing Backend Dependencies...
cd backend
pip install -r requirements.txt

echo.
echo Installing Camera Service Dependencies...
cd ../camera_service
pip install -r requirements.txt

echo.
echo Installing Frontend Dependencies...
cd ../frontend
call npm install

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Open 3 terminals/command prompts
echo 2. In Terminal 1: Run start_backend.bat
echo 3. In Terminal 2: Run start_frontend.bat
echo 4. In Terminal 3: Run start_camera_service.bat
echo.
pause
