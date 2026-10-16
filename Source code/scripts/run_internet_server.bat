@echo off
setlocal
cd /d "%~dp0\.."
set /p DM_RELAY_PASSWORD=Enter relay demonstration password: 
python run_relay_server.py --host 0.0.0.0 --port 9876 --password "%DM_RELAY_PASSWORD%"
endlocal
