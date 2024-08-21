@echo off

REM Step 1: Pull the project
git pull origin agas9

REM Step 2: Change to the project directory
cd agas9

REM Step 3: Checkout the relevant branch
git checkout agas9

REM Step 4: Create a virtual environment
python -m venv .venv

REM Step 5: Activate the virtual environment
.\.venv\Scripts\activate

REM Step 6: Install the relevant packages
pip install -r requirements.txt

REM Step 7: Run the wsgi.py script
python wsgi.py

@echo on
