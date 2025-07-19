#!/bin/bash

# PythonAnywhere Deployment Script for InfluHaat
# Run this script in your PythonAnywhere Bash console

echo "Starting InfluHaat deployment on PythonAnywhere..."

# Navigate to project directory
cd ~/infu_haat

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3.11 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install/upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Create database directory if it doesn't exist
mkdir -p ~/infu_haat

# Initialize database
echo "Initializing database..."
python -c "
from app import app, db
with app.app_context():
    db.create_all()
    print('Database initialized successfully!')
"

# Create uploads directory
mkdir -p uploads

# Set permissions
chmod 755 uploads

echo "Deployment completed!"
echo "Next steps:"
echo "1. Configure your web app in the PythonAnywhere Web tab"
echo "2. Update the WSGI file with your username"
echo "3. Set up static files mapping"
echo "4. Reload your web app"
echo "5. Visit your website at yourusername.pythonanywhere.com" 