@echo off
setlocal
cd /d "%~dp0"
if not exist source\run_desktop_messenger.py (
  echo Missing Published\source. Recreate Desktop_Messenger_Portable_Source.zip or copy Source code here.
  exit /b 1
)
python -m venv .build_venv
call .build_venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m PyInstaller --noconfirm DesktopMessenger.spec
echo Build complete. Validate dist\DesktopMessenger on Windows before submission.
endlocal
