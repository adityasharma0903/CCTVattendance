@echo off
echo ========================================
echo Installing with Virtual Environment
echo ========================================
echo.

REM Create virtual environment for backend
echo Creating backend virtual environment...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
echo Installing backend dependencies...
pip install --upgrade pip
pip install -r requirements.txt
call deactivate
cd ..
echo Backend virtual environment created successfully!
echo.

REM Create virtual environment for camera service
echo Creating camera service virtual environment...
cd camera_service
python -m venv venv
call venv\Scripts\activate.bat
echo Installing camera service dependencies...
pip install --upgrade pip
pip install -r requirements.txt
call deactivate
cd ..
echo Camera service virtual environment created successfully!
echo.

REM Install frontend dependencies
echo Installing Frontend Dependencies...
cd frontend
call npm install
cd ..
echo.

echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo IMPORTANT: Virtual environments created!
echo Use the new start scripts:
echo   - start_backend_venv.bat
echo   - start_camera_service_venv.bat
echo   - start_frontend.bat (unchanged)
echo.
pause

