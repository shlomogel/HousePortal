@echo off
setlocal enabledelayedexpansion

<<<<<<< Updated upstream
=======
REM Check if Git is installed
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo Git is not installed or not in the system PATH.
    
    echo Detected architecture: %PROCESSOR_ARCHITECTURE%
    
    if "%PROCESSOR_ARCHITECTURE:~-2%"=="64" (
        echo 64-bit system detected.
        set "GITINSTALLER=Git-2.46.0-64-bit.exe"
    ) else (
        echo 32-bit system detected.
        set "GITINSTALLER=Git-2.46.0-32-bit.exe"
    )
    
    echo Installer selected: !GITINSTALLER!
    
    if exist "%~dp0!GITINSTALLER!" (
        echo Installing Git...
        start "" /wait "%~dp0!GITINSTALLER!"
        echo Please complete the Git installation process.
        echo After installation, you may need to restart your computer.
        echo Once Git is installed, the script will continue.
        pause
    ) else (
        echo Git installer not found: !GITINSTALLER!
        echo Please download and install Git manually from https://git-scm.com/download/win
        pause
        exit /b 1
    )
)

>>>>>>> Stashed changes
REM Step 1: Clone the project (if it doesn't exist)
if not exist HousePortal (
    git clone https://github.com/shlomogel/HousePortal.git Agas9
    echo Project cloned successfully.
) else (
    echo Project directory already exists.
)

REM Step 2: Change to the project directory
cd Agas9
<<<<<<< Updated upstream
mkdir logs
=======
if not exist logs mkdir logs
>>>>>>> Stashed changes

REM Step 3: Fetch the latest changes
git fetch origin

REM Step 4: Checkout and pull the agas9 branch
git checkout agas9
git pull origin agas9

REM Step 5: Create a virtual environment (if it doesn't exist)
if not exist .venv\ (
    python -m venv .venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

REM Step 6: Activate the virtual environment
call .venv\Scripts\activate

REM Step 7: Install or upgrade the relevant packages
pip install -r requirements.txt

REM Step 8: Run the wsgi.py script
python wsgi.py

endlocal