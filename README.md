# InfluHaat - B2B Influencer Marketplace

A modern web application that connects businesses with influencers for marketing campaigns. Built with Flask, featuring location-based and category-specific influencer discovery.

## Features

- **Business Registration & Dashboard**: Companies can register, create profiles, and manage influencer contacts
- **Influencer Registration & Dashboard**: Influencers can showcase their profiles, rates, and manage incoming requests
- **Advanced Search**: Filter influencers by location, category, follower count, and budget
- **Contact System**: Direct messaging between businesses and influencers
- **Responsive Design**: Modern, mobile-friendly interface
- **Category-Based Matching**: Industry-specific influencer discovery

## Technology Stack

- **Backend**: Python 3.11, Flask
- **Database**: SQLite (with SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF, WTForms

## Installation & Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package installer)

### Step 1: Clone or Download the Project

```bash
# If using git
git clone <repository-url>
cd infu_haat

# Or simply navigate to your project directory
cd infu_haat
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## How to Use the Application

### For Businesses

1. **Register**: Go to the homepage and click "Join as Business"
2. **Complete Profile**: Fill in your company details, industry, and location
3. **Search Influencers**: Use the search filters to find relevant influencers
4. **Contact**: Send messages to influencers with your campaign details
5. **Manage**: View all your contacts in the business dashboard

### For Influencers

1. **Register**: Go to the homepage and click "Join as Influencer"
2. **Complete Profile**: Add your bio, categories, follower count, and rates
3. **Get Discovered**: Businesses will find you through search filters
4. **Manage Requests**: View and respond to incoming business contacts

### Search Features

- **Location-based**: Find influencers in specific cities or regions
- **Category-specific**: Filter by industry (Technology, Fashion, Food, etc.)
- **Budget-friendly**: Set maximum budget constraints
- **Follower count**: Filter by minimum follower requirements

## Database Structure

The application uses SQLite with the following main tables:

- **Users**: Authentication and user type (business/influencer)
- **Businesses**: Company profiles and contact information
- **Influencers**: Influencer profiles, rates, and social media details
- **Contacts**: Messages and campaign requests between businesses and influencers

## File Structure

```
infu_haat/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template with navigation
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── register_business.html
│   ├── register_influencer.html
│   ├── business_dashboard.html
│   ├── influencer_dashboard.html
│   ├── search_results.html
│   ├── influencer_profile.html
│   └── contact_form.html
└── influencer_marketplace.db  # SQLite database (created automatically)
```

## Customization

### Adding New Business Categories

Edit the `business_type` choices in `app.py`:

```python
business_type = SelectField('Business Type', choices=[
    ('technology', 'Technology'),
    ('fashion', 'Fashion & Beauty'),
    # Add your new category here
    ('your_category', 'Your Category Name'),
])
```

### Adding New Influencer Categories

Edit the `categories` choices in `app.py`:

```python
categories = SelectField('Primary Category', choices=[
    ('technology', 'Technology'),
    ('fashion', 'Fashion & Beauty'),
    # Add your new category here
    ('your_category', 'Your Category Name'),
])
```

### Styling

The application uses Bootstrap 5 with custom CSS variables. Main colors can be modified in `templates/base.html`:

```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    --accent-color: #f093fb;
}
```

## Security Notes

- Change the `SECRET_KEY` in `app.py` for production use
- Consider using environment variables for sensitive configuration
- Implement proper email verification for production
- Add rate limiting for contact forms
- Use HTTPS in production

## Production Deployment

For production deployment, consider:

1. **Web Server**: Use Gunicorn or uWSGI with Nginx
2. **Database**: Switch to PostgreSQL or MySQL
3. **Environment**: Use environment variables for configuration
4. **Security**: Enable HTTPS, add CSRF protection
5. **Monitoring**: Add logging and error tracking

## Troubleshooting

### Common Issues

1. **Port already in use**: Change the port in `app.py` or kill the existing process
2. **Database errors**: Delete `influencer_marketplace.db` and restart the app
3. **Import errors**: Ensure all dependencies are installed with `pip install -r requirements.txt`

### Getting Help

If you encounter issues:

1. Check that Python 3.11+ is installed
2. Verify all dependencies are installed
3. Check the console for error messages
4. Ensure you're in the correct directory when running the app

## License

This project is open source and available under the MIT License.

---

**InfluHaat** - Connecting businesses with the right influencers for successful marketing campaigns. 