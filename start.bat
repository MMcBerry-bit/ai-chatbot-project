@echo off
REM Quick Start Script for AI Chatbot
REM Dorcas Innovations LLC

echo ========================================
echo AI Chatbot - Quick Start
echo Dorcas Innovations LLC
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.13+ from python.org
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import openai" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements_app.txt
)

echo.
echo Dependencies ready!
echo.

REM Check for GitHub token
if "%GITHUB_TOKEN%"=="" (
    echo WARNING: GITHUB_TOKEN environment variable not set
    echo.
    echo Please set your GitHub token:
    echo   set GITHUB_TOKEN=your_token_here
    echo.
    echo Or get one at: https://github.com/settings/tokens
    echo.
    pause
)

echo.
echo Choose version to run:
echo 1. Console Version (Simple CLI)
echo 2. Desktop GUI (Store-Ready)
echo 3. Web Version (Streamlit)
echo 4. Exit
echo.

set /p choice="Enter choice (1-4): "

if "%choice%"=="1" (
    echo Starting Console Version...
    python src\ai_chatbot.py
)
if "%choice%"=="2" (
    echo Starting Desktop GUI...
    python src\chatbot_store_ready.py
)
if "%choice%"=="3" (
    echo Starting Web Version...
    streamlit run src\chatbot_web.py
)
if "%choice%"=="4" (
    exit /b 0
)

pause
