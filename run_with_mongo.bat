@echo off
cd /d "%~dp0"
echo Starting Video Tracker...
echo Ensure you have a .env file with your MONGO_URI set.
python app.py
pause
