@echo off
echo ========================================
echo   Meeting Notes to PDF - Setup
echo ========================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Ollama
ollama --version >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Ollama is not installed.
    echo Download from: https://ollama.com/download
    echo.
    echo After installing, run:
    echo   ollama pull llama3.1
    echo.
)

REM Install Python dependencies
echo Installing Python dependencies...
pip install fpdf2 requests ollama flask
echo.

echo ========================================
echo   Setup complete!
echo ========================================
echo.
echo To run the app:
echo   python app.py          (desktop GUI)
echo   python web_app.py      (web UI)
echo.
echo To install a model (if not already installed):
echo   ollama pull llama3.1
echo.
pause
