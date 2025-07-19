# InfluHaat - PythonAnywhere Deployment

## Quick Start

1. **Upload your code** to PythonAnywhere
2. **Run the deployment script**:
   ```bash
   chmod +x deploy_pythonanywhere.sh
   ./deploy_pythonanywhere.sh
   ```
3. **Configure your web app** in the PythonAnywhere Web tab
4. **Update the WSGI file** with your username
5. **Reload your web app**

## Important Files

- `app.py` - Main Flask application
- `wsgi.py` - WSGI configuration for PythonAnywhere
- `pythonanywhere_config.py` - Configuration settings
- `deploy_pythonanywhere.sh` - Automated deployment script
- `PYTHONANYWHERE_DEPLOYMENT.md` - Detailed deployment guide

## Configuration

Before deploying, update these files with your PythonAnywhere username:

1. `pythonanywhere_config.py` - Replace `yourusername` with your actual username
2. `wsgi.py` - Replace `yourusername` with your actual username
3. `app.py` - The database path will be automatically configured

## Security

- Change the `SECRET_KEY` in both `pythonanywhere_config.py` and `wsgi.py`
- Use environment variables for sensitive data
- Consider upgrading to a paid plan for HTTPS

## Support

- See `PYTHONANYWHERE_DEPLOYMENT.md` for detailed instructions
- Check PythonAnywhere error logs for troubleshooting
- Visit: https://help.pythonanywhere.com/

## Your Website

After deployment, your website will be available at:
`https://yourusername.pythonanywhere.com` 