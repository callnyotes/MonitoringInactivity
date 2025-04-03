@echo off
echo Starting Flask app in a new window...
cd /d "C:\Users\F7OUTO9\PycharmProjects\MonitoringActivity"
start "Flask App" cmd /c "venv\Scripts\python.exe app.py"
timeout /t 5 >nul
echo Opening application in Chrome...
start chrome http://127.0.0.1:5001