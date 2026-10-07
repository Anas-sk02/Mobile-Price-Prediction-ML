@echo off
title SmartPrice - College ML Lab Project
echo ======================================================================
echo           SmartPrice - ML Price Prediction & Benchmarking
echo               College Machine Learning Lab Project
echo ======================================================================
echo.

echo [1/3] Checking Python & Node dependencies...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH. Please install Python 3.10+.
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH. Please install Node.js.
    pause
    exit /b 1
)

echo [2/3] Starting FastAPI ML Backend (Port 8000)...
start "SmartPrice ML Backend" cmd /k "python run_backend.py"

echo [3/3] Starting React Web Dashboard (Port 3000)...
start "SmartPrice Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ======================================================================
echo System successfully initialized!
echo - Web Dashboard:  http://localhost:3000
echo - Backend API:     http://localhost:8000
echo - Swagger Docs:    http://localhost:8000/docs
echo ======================================================================
echo.
echo Opening browser in 3 seconds...
timeout /t 3 /nobreak >nul
start http://localhost:3000

echo.
echo Press any key to close this launcher window (Servers will stay running).
pause >nul
