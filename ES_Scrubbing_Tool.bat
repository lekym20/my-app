@echo off
title ES Scrubbing Tool

cd /d "%~dp0"

echo.
echo ==========================================
echo ES Scrubbing Tool
echo ==========================================
echo.

where py >nul 2>&1

if errorlevel 1 (
    echo.
    echo ERROR:
    echo Python launcher not found.
    echo Please install Python.
    echo.
    pause
    exit /b 1
)

python main.py

echo.
echo ==========================================
echo Process Finished
echo ==========================================
echo.

pause