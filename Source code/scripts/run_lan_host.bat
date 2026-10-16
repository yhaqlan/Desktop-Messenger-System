@echo off
setlocal
cd /d "%~dp0\.."
python run_lan_host.py --host 0.0.0.0 --port 8765
endlocal
