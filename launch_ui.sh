#!/bin/bash

# Launch Cryptocurrency Intelligence Platform UI
# This script sets up and launches the Streamlit web application

echo "================================================"
echo "  Cryptocurrency Intelligence Platform UI"
echo "================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if requirements are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "⚠️  Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
    echo ""
else
    echo "✅ Dependencies already installed"
    echo ""
fi

# Check if clustered data exists
if [ ! -f "clustered_crypto_data.csv" ]; then
    echo "⚠️  WARNING: clustered_crypto_data.csv not found"
    echo ""
    echo "Please run the Jupyter notebook first:"
    echo "  1. jupyter notebook crypto_clustering.ipynb"
    echo "  2. Run all cells"
    echo "  3. Add and run this cell:"
    echo ""
    echo "     from export_data_for_app import export_clustered_data"
    echo "     export_clustered_data(clustered_df)"
    echo ""
    echo "The app will use sample data for now..."
    echo ""
    read -p "Press Enter to continue with sample data..."
fi

echo "🚀 Launching Streamlit app..."
echo ""
echo "The app will open in your browser at: http://localhost:8501"
echo ""
echo "To stop the app, press Ctrl+C"
echo ""
echo "================================================"
echo ""

# Launch Streamlit
streamlit run app.py
