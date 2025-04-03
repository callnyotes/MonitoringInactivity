@echo off
echo Stopping the Flask app...
for /f "tokens=5" %%a in ('netstat -ano ^| find ":5001" ^| find "LISTENING"') do (
    echo Killing process with PID %%a...
    taskkill /PID %%a /F
)

echo Starting the Flask app...
start python app.py
pause