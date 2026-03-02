#!/bin/bash
# Render Build Script - Runs during build phase
# This installs dependencies and prepares the application for deployment

echo "======================================================================"
echo "Building AHJ Engine Application"
echo "======================================================================"

# Install Python dependencies
echo "[1/3] Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Create necessary directories
echo "[2/3] Creating application directories..."
mkdir -p app/data/master
mkdir -p logs
mkdir -p static

# Run database initialization
echo "[3/3] Initializing database..."
python init_db_full.py

echo "======================================================================"
echo "✓ Build completed successfully"
echo "======================================================================"
