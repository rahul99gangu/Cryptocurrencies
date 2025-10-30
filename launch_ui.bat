@echo off
REM Launch Cryptocurrency Intelligence Platform UI (Windows)

echo ================================================
echo   Cryptocurrency Intelligence Platform UI
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo Python found
echo.

REM Check if requirements are installed
echo Checking dependencies...
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo Streamlit not found. Installing dependencies...
    pip install -r requirements.txt
    echo.
) else (
    echo Dependencies already installed
    echo.
)

REM Check if clustered data exists
if not exist "clustered_crypto_data.csv" (
    echo WARNING: clustered_crypto_data.csv not found
    echo.
    echo Please run the Jupyter notebook first:
    echo   1. jupyter notebook crypto_clustering.ipynb
    echo   2. Run all cells
    echo   3. Add and run this cell:
    echo.
    echo      from export_data_for_app import export_clustered_data
    echo      export_clustered_data(clustered_df^)
    echo.
    echo The app will use sample data for now...
    echo.
    pause
)

echo Launching Streamlit app...
echo.
echo The app will open in your browser at: http://localhost:8501
echo.
echo To stop the app, press Ctrl+C
echo.
echo ================================================
echo.

REM Launch Streamlit
streamlit run app.py
