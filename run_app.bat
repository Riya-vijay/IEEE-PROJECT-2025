@echo off
echo Starting ATME College Assistant...
echo.
echo Step 1: Starting Backend Server...
start cmd /k "python backend.py"
echo Backend server starting on http://localhost:5000
echo.
timeout /t 3
echo.
echo Step 2: Starting Frontend Application...
streamlit run frontend.py
