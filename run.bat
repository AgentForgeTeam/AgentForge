@echo off
REM ===========================================================
REM  Agent Forge - launcher for Windows
REM  Creates a virtual environment on first run, then starts.
REM  Messages are in Latin script on purpose: the Windows
REM  console uses a legacy code page and would garble UTF-8.
REM ===========================================================
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo.
    echo  ERROR: Python not found.
    echo  Install Python 3.11+ from https://www.python.org/downloads/
    echo  and tick "Add Python to PATH" during setup.
    echo.
    pause
    exit /b 1
)

python -c "import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)"
if errorlevel 1 (
    echo.
    echo  ERROR: Python 3.11 or newer is required.
    python --version
    echo.
    pause
    exit /b 1
)

if not exist ".venv" (
    echo.
    echo  Creating virtual environment (.venv)...
    python -m venv .venv
    if errorlevel 1 (
        echo  ERROR: failed to create the virtual environment.
        pause
        exit /b 1
    )
    ".venv\Scripts\python.exe" -m pip install --upgrade pip --quiet
    echo  Installing dependencies, this takes a few minutes...
    ".venv\Scripts\pip.exe" install -r requirements.txt
    if errorlevel 1 (
        echo  ERROR: failed to install dependencies.
        pause
        exit /b 1
    )
    echo  Done.
    echo.
)

".venv\Scripts\python.exe" main.py %*
if errorlevel 1 (
    echo.
    echo  The application exited with an error.
    echo  See the log: %%APPDATA%%\agent-forge\logs\app.log
    pause
)
