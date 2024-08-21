@echo off
setlocal

REM Set the directory of your HTML files
set "DIR=C:\Users\shlomog\OneDrive - Mobileye\Desktop\Agas9\AgasPortal"

REM Change to the directory
cd /d "%DIR%"
.venv\Scripts\activate
flask --app agas_portal run

REM Start the Python HTTP server
echo Starting local server at http://127.0.0.1:5000
python -m http.server 8000

endlocal
pause
