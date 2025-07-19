import sys
import os

# Add your project directory to the sys.path
path = '/home/yourusername/infu_haat'
if path not in sys.path:
    sys.path.append(path)

# Set environment variables
os.environ['PYTHONANYWHERE_SITE'] = 'True'
os.environ['SECRET_KEY'] = 'your-super-secret-key-change-this-in-production'

# Import your Flask app
from app import app as application

# For debugging
if __name__ == "__main__":
    application.run() 