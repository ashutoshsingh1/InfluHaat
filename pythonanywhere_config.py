# PythonAnywhere Configuration
# This file contains settings specific to PythonAnywhere deployment

import os

# Database configuration for PythonAnywhere
PYTHONANYWHERE_DATABASE_PATH = '/home/yourusername/infu_haat/infu_haat.db'

# Secret key for production (change this!)
SECRET_KEY = 'your-super-secret-key-change-this-in-production'

# Debug mode (set to False in production)
DEBUG = False

# Host and port configuration
HOST = '0.0.0.0'
PORT = 5000

# Email configuration (if needed)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = 'your-email@gmail.com'
MAIL_PASSWORD = 'your-app-password'

# File upload settings
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
UPLOAD_FOLDER = '/home/yourusername/infu_haat/uploads'

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FILE = '/home/yourusername/infu_haat/app.log' 