# PythonAnywhere Deployment Guide for InfluHaat

## Prerequisites
- PythonAnywhere account (free or paid)
- Basic knowledge of PythonAnywhere interface

## Step 1: Upload Your Code

### Option A: Using Git (Recommended)
1. Open a Bash console on PythonAnywhere
2. Navigate to your home directory:
   ```bash
   cd ~
   ```
3. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/infu_haat.git
   cd infu_haat
   ```

### Option B: Manual Upload
1. Go to the Files tab on PythonAnywhere
2. Create a new directory called `infu_haat`
3. Upload all your project files to this directory

## Step 2: Set Up Virtual Environment

1. Open a Bash console and navigate to your project:
   ```bash
   cd ~/infu_haat
   ```

2. Create a virtual environment:
   ```bash
   python3.11 -m venv venv
   ```

3. Activate the virtual environment:
   ```bash
   source venv/bin/activate
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Step 3: Configure the Application

1. Edit `pythonanywhere_config.py`:
   - Replace `yourusername` with your actual PythonAnywhere username
   - Change the `SECRET_KEY` to a secure random string
   - Update email settings if needed

2. Update `app.py` database path:
   - Make sure the database path points to your actual username

## Step 4: Set Up the Web App

1. Go to the Web tab on PythonAnywhere
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.11
5. Set the source code directory to `/home/yourusername/infu_haat`

## Step 5: Configure WSGI File

1. Click on the WSGI configuration file link
2. Replace the content with:

```python
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
```

## Step 6: Initialize Database

1. Open a Bash console
2. Navigate to your project and activate virtual environment:
   ```bash
   cd ~/infu_haat
   source venv/bin/activate
   ```

3. Run Python and create the database:
   ```python
   python
   >>> from app import app, db
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```

## Step 7: Configure Static Files

1. In the Web tab, go to "Static files"
2. Add static file mappings:
   - URL: `/static/`
   - Directory: `/home/yourusername/infu_haat/static`

## Step 8: Set Up Environment Variables

1. In the Web tab, go to "Environment variables"
2. Add the following variables:
   - `SECRET_KEY`: Your secret key
   - `PYTHONANYWHERE_SITE`: `True`

## Step 9: Reload the Web App

1. Click the "Reload" button in the Web tab
2. Your app should now be accessible at `yourusername.pythonanywhere.com`

## Step 10: Test Your Application

1. Visit your website URL
2. Test registration and login functionality
3. Check if the database is working properly

## Troubleshooting

### Common Issues:

1. **Import Errors**: Make sure all dependencies are installed in your virtual environment
2. **Database Errors**: Check that the database path is correct and the directory exists
3. **Static Files Not Loading**: Verify static file mappings in the Web tab
4. **Permission Errors**: Make sure your PythonAnywhere username is correct in all paths

### Debug Mode:
- For debugging, set `DEBUG = True` in `pythonanywhere_config.py`
- Check the error logs in the Web tab

### Logs:
- Check the error logs in the Web tab for detailed error messages
- Use the console to run Python commands and debug issues

## Security Considerations

1. **Change the Secret Key**: Use a strong, random secret key
2. **Environment Variables**: Store sensitive data in environment variables
3. **HTTPS**: Consider upgrading to a paid plan for HTTPS support
4. **Database Security**: Regularly backup your database

## Maintenance

1. **Regular Updates**: Keep your dependencies updated
2. **Backups**: Regularly backup your database and code
3. **Monitoring**: Check your app's performance and error logs

## Support

- PythonAnywhere Documentation: https://help.pythonanywhere.com/
- Flask Documentation: https://flask.palletsprojects.com/
- For issues specific to this app, check the error logs and console output

## File Structure After Deployment

```
/home/yourusername/infu_haat/
├── app.py
├── requirements.txt
├── pythonanywhere_config.py
├── infu_haat.db
├── venv/
├── templates/
├── static/
└── uploads/
```

Your app will be accessible at: `https://yourusername.pythonanywhere.com` 