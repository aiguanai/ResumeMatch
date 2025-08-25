@echo off
echo Resume Matching API - Server Startup
echo ====================================

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo Creating .env file from template...
    copy env_example.txt .env
    echo Please edit .env file and add your OpenAI API key
    pause
    exit /b 1
)

REM Start the server
echo Starting Resume Matching API server...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python app.py

pause
