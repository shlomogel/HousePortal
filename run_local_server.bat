@echo off

REM Step 1: Clone the project (if it doesn't exist)
if not exist HousePortal (
    git clone https://github.com/shlomogel/HousePortal.git Agas9
    echo Project cloned successfully.
) else (
    echo Project directory already exists.
)

REM Step 2: Change to the project directory
cd Agas9
mkdir logs

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

@echo on
