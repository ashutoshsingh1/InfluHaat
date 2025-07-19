from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///influencer_marketplace.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # 'business' or 'influencer'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Business(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    business_type = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    contact_person = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    website = db.Column(db.String(200))
    
    # Relationships
    user = db.relationship('User', backref='business_profile')

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    categories = db.Column(db.String(200), nullable=False)  # Comma-separated
    location = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text)
    followers_count = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Float, default=0.0)
    platforms = db.Column(db.String(200))  # Comma-separated
    rate_per_post = db.Column(db.Float, default=0.0)
    portfolio_url = db.Column(db.String(200))
    
    # Relationships
    user = db.relationship('User', backref='influencer_profile')

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    budget = db.Column(db.Float)
    campaign_type = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    business = db.relationship('Business', backref='contacts')
    influencer = db.relationship('Influencer', backref='contacts')

class ContactResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=False)
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=True)  # For business responses
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # 'accepted', 'declined', 'counter_offer', 'business_counter'
    counter_offer = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    contact = db.relationship('Contact', backref='responses')
    influencer = db.relationship('Influencer', backref='responses')
    business = db.relationship('Business', backref='responses')

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewed_business_id = db.Column(db.Integer, db.ForeignKey('business.id'), nullable=True)
    reviewed_influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id'), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    title = db.Column(db.String(200), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reviewer = db.relationship('User', backref='reviews_given')
    reviewed_business = db.relationship('Business', backref='reviews_received')
    reviewed_influencer = db.relationship('Influencer', backref='reviews_received')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Forms
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BusinessRegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    company_name = StringField('Company Name', validators=[DataRequired()])
    business_type = SelectField('Business Type', choices=[
        ('technology', 'Technology'),
        ('fashion', 'Fashion & Beauty'),
        ('food', 'Food & Beverage'),
        ('fitness', 'Health & Fitness'),
        ('travel', 'Travel & Tourism'),
        ('finance', 'Finance'),
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('automotive', 'Automotive'),
        ('real_estate', 'Real Estate'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    contact_person = StringField('Contact Person', validators=[DataRequired()])
    description = TextAreaField('Business Description')
    phone = StringField('Phone Number')
    website = StringField('Website URL')
    submit = SubmitField('Register')

class InfluencerRegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    name = StringField('Full Name', validators=[DataRequired()])
    categories = SelectField('Primary Category', choices=[
        ('technology', 'Technology'),
        ('fashion', 'Fashion & Beauty'),
        ('food', 'Food & Beverage'),
        ('fitness', 'Health & Fitness'),
        ('travel', 'Travel & Tourism'),
        ('lifestyle', 'Lifestyle'),
        ('gaming', 'Gaming'),
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('business', 'Business'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    bio = TextAreaField('Bio')
    followers_count = StringField('Followers Count (approximate)')
    platforms = StringField('Social Media Platforms (comma-separated)')
    rate_per_post = StringField('Rate per Post (₹)')
    portfolio_url = StringField('Portfolio/Profile URL')
    submit = SubmitField('Register')

class ContactForm(FlaskForm):
    message = TextAreaField('Message', validators=[DataRequired()])
    budget = StringField('Budget (₹)')
    campaign_type = SelectField('Campaign Type', choices=[
        ('sponsored_post', 'Sponsored Post'),
        ('product_review', 'Product Review'),
        ('brand_ambassador', 'Brand Ambassador'),
        ('event_promotion', 'Event Promotion'),
        ('giveaway', 'Giveaway/Contest'),
        ('other', 'Other')
    ])
    submit = SubmitField('Send Message')

class ContactResponseForm(FlaskForm):
    message = TextAreaField('Response Message', validators=[DataRequired()])
    status = SelectField('Response', choices=[
        ('accepted', 'Accept Offer'),
        ('declined', 'Decline Offer'),
        ('counter_offer', 'Make Counter Offer')
    ], validators=[DataRequired()])
    counter_offer = StringField('Counter Offer Amount (₹)')
    submit = SubmitField('Send Response')

class BusinessResponseForm(FlaskForm):
    message = TextAreaField('Response Message', validators=[DataRequired()])
    status = SelectField('Response', choices=[
        ('accepted', 'Accept Counter Offer'),
        ('declined', 'Decline Counter Offer'),
        ('business_counter', 'Make New Counter Offer')
    ], validators=[DataRequired()])
    counter_offer = StringField('New Counter Offer Amount (₹)')
    submit = SubmitField('Send Response')

class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[
        (5, '⭐⭐⭐⭐⭐ Excellent'),
        (4, '⭐⭐⭐⭐ Very Good'),
        (3, '⭐⭐⭐ Good'),
        (2, '⭐⭐ Fair'),
        (1, '⭐ Poor')
    ], coerce=int, validators=[DataRequired()])
    title = StringField('Review Title', validators=[DataRequired(), Length(min=5, max=200)])
    comment = TextAreaField('Review Comment', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Submit Review')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            if user.user_type == 'business':
                return redirect(url_for('business_dashboard'))
            else:
                return redirect(url_for('influencer_dashboard'))
        flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/register/business', methods=['GET', 'POST'])
def register_business():
    form = BusinessRegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered')
            return render_template('register_business.html', form=form)
        
        user = User(
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            user_type='business'
        )
        db.session.add(user)
        db.session.commit()
        
        business = Business(
            user_id=user.id,
            company_name=form.company_name.data,
            business_type=form.business_type.data,
            location=form.location.data,
            contact_person=form.contact_person.data,
            description=form.description.data,
            phone=form.phone.data,
            website=form.website.data
        )
        db.session.add(business)
        db.session.commit()
        
        login_user(user)
        flash('Registration successful!')
        return redirect(url_for('business_dashboard'))
    
    return render_template('register_business.html', form=form)

@app.route('/register/influencer', methods=['GET', 'POST'])
def register_influencer():
    form = InfluencerRegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered')
            return render_template('register_influencer.html', form=form)
        
        user = User(
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            user_type='influencer'
        )
        db.session.add(user)
        db.session.commit()
        
        followers = 0
        try:
            followers = int(form.followers_count.data) if form.followers_count.data else 0
        except:
            followers = 0
        
        rate = 0.0
        try:
            rate = float(form.rate_per_post.data) if form.rate_per_post.data else 0.0
        except:
            rate = 0.0
        
        influencer = Influencer(
            user_id=user.id,
            name=form.name.data,
            categories=form.categories.data,
            location=form.location.data,
            bio=form.bio.data,
            followers_count=followers,
            platforms=form.platforms.data,
            rate_per_post=rate,
            portfolio_url=form.portfolio_url.data
        )
        db.session.add(influencer)
        db.session.commit()
        
        login_user(user)
        flash('Registration successful!')
        return redirect(url_for('influencer_dashboard'))
    
    return render_template('register_influencer.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/business/dashboard')
@login_required
def business_dashboard():
    if current_user.user_type != 'business':
        return redirect(url_for('index'))
    
    business = Business.query.filter_by(user_id=current_user.id).first()
    contacts = Contact.query.filter_by(business_id=business.id).all()
    return render_template('business_dashboard.html', business=business, contacts=contacts)

@app.route('/influencer/dashboard')
@login_required
def influencer_dashboard():
    if current_user.user_type != 'influencer':
        return redirect(url_for('index'))
    
    influencer = Influencer.query.filter_by(user_id=current_user.id).first()
    contacts = Contact.query.filter_by(influencer_id=influencer.id).all()
    return render_template('influencer_dashboard.html', influencer=influencer, contacts=contacts)

@app.route('/search')
def search_influencers():
    location = request.args.get('location', '')
    category = request.args.get('category', '')
    min_followers = request.args.get('min_followers', '')
    max_budget = request.args.get('max_budget', '')
    
    query = Influencer.query
    
    if location:
        query = query.filter(Influencer.location.ilike(f'%{location}%'))
    if category:
        query = query.filter(Influencer.categories.ilike(f'%{category}%'))
    if min_followers:
        try:
            query = query.filter(Influencer.followers_count >= int(min_followers))
        except:
            pass
    if max_budget:
        try:
            query = query.filter(Influencer.rate_per_post <= float(max_budget))
        except:
            pass
    
    influencers = query.all()
    return render_template('search_results.html', influencers=influencers, 
                         location=location, category=category, 
                         min_followers=min_followers, max_budget=max_budget)



@app.route('/influencer/<int:id>')
def influencer_profile(id):
    influencer = Influencer.query.get_or_404(id)
    
    # Get reviews for this influencer
    reviews = Review.query.filter_by(reviewed_influencer_id=id).order_by(Review.created_at.desc()).limit(3).all()
    
    # Calculate average rating
    all_reviews = Review.query.filter_by(reviewed_influencer_id=id).all()
    if all_reviews:
        avg_rating = sum(review.rating for review in all_reviews) / len(all_reviews)
        total_reviews = len(all_reviews)
    else:
        avg_rating = 0
        total_reviews = 0
    
    # Check if current user can review this influencer
    can_review = False
    if current_user.is_authenticated and current_user.user_type == 'business':
        existing_review = Review.query.filter_by(
            reviewer_id=current_user.id,
            reviewed_influencer_id=id
        ).first()
        can_review = not existing_review
    
    return render_template('influencer_profile.html', 
                         influencer=influencer, 
                         reviews=reviews, 
                         avg_rating=avg_rating, 
                         total_reviews=total_reviews,
                         can_review=can_review)

@app.route('/business/<int:id>')
def business_profile(id):
    business = Business.query.get_or_404(id)
    
    # Get reviews for this business
    reviews = Review.query.filter_by(reviewed_business_id=id).order_by(Review.created_at.desc()).limit(3).all()
    
    # Calculate average rating
    all_reviews = Review.query.filter_by(reviewed_business_id=id).all()
    if all_reviews:
        avg_rating = sum(review.rating for review in all_reviews) / len(all_reviews)
        total_reviews = len(all_reviews)
    else:
        avg_rating = 0
        total_reviews = 0
    
    # Check if current user can review this business
    can_review = False
    if current_user.is_authenticated and current_user.user_type == 'influencer':
        existing_review = Review.query.filter_by(
            reviewer_id=current_user.id,
            reviewed_business_id=id
        ).first()
        can_review = not existing_review
    
    return render_template('business_profile.html', 
                         business=business, 
                         reviews=reviews, 
                         avg_rating=avg_rating, 
                         total_reviews=total_reviews,
                         can_review=can_review)

@app.route('/contact/<int:influencer_id>', methods=['GET', 'POST'])
@login_required
def contact_influencer(influencer_id):
    if current_user.user_type != 'business':
        flash('Only businesses can contact influencers')
        return redirect(url_for('index'))
    
    business = Business.query.filter_by(user_id=current_user.id).first()
    influencer = Influencer.query.get_or_404(influencer_id)
    form = ContactForm()
    
    if form.validate_on_submit():
        budget = 0.0
        try:
            budget = float(form.budget.data) if form.budget.data else 0.0
        except:
            budget = 0.0
        
        contact = Contact(
            business_id=business.id,
            influencer_id=influencer_id,
            message=form.message.data,
            budget=budget,
            campaign_type=form.campaign_type.data
        )
        db.session.add(contact)
        db.session.commit()
        
        flash('Message sent successfully!')
        return redirect(url_for('business_dashboard'))
    
    return render_template('contact_form.html', form=form, influencer=influencer)

@app.route('/contact-business/<int:business_id>', methods=['GET', 'POST'])
@login_required
def contact_business(business_id):
    if current_user.user_type != 'influencer':
        flash('Only influencers can contact businesses')
        return redirect(url_for('index'))
    
    influencer = Influencer.query.filter_by(user_id=current_user.id).first()
    business = Business.query.get_or_404(business_id)
    form = ContactForm()
    
    if form.validate_on_submit():
        budget = 0.0
        try:
            budget = float(form.budget.data) if form.budget.data else 0.0
        except:
            budget = 0.0
        
        contact = Contact(
            business_id=business_id,
            influencer_id=influencer.id,
            message=form.message.data,
            budget=budget,
            campaign_type=form.campaign_type.data
        )
        db.session.add(contact)
        db.session.commit()
        
        flash('Message sent successfully!')
        return redirect(url_for('influencer_dashboard'))
    
    return render_template('contact_business_form.html', form=form, business=business)

@app.route('/respond/<int:contact_id>', methods=['GET', 'POST'])
@login_required
def respond_to_contact(contact_id):
    if current_user.user_type != 'influencer':
        flash('Only influencers can respond to contacts')
        return redirect(url_for('index'))
    
    contact = Contact.query.get_or_404(contact_id)
    influencer = Influencer.query.filter_by(user_id=current_user.id).first()
    
    # Check if this contact is for the current influencer
    if contact.influencer_id != influencer.id:
        flash('You can only respond to contacts sent to you')
        return redirect(url_for('influencer_dashboard'))
    
    # Check if already responded
    existing_response = ContactResponse.query.filter_by(contact_id=contact_id, influencer_id=influencer.id).first()
    if existing_response:
        flash('You have already responded to this contact')
        return redirect(url_for('influencer_dashboard'))
    
    form = ContactResponseForm()
    
    if form.validate_on_submit():
        counter_offer = None
        if form.status.data == 'counter_offer':
            try:
                counter_offer = float(form.counter_offer.data) if form.counter_offer.data else None
            except:
                flash('Invalid counter offer amount')
                return render_template('respond_to_contact.html', form=form, contact=contact)
        
        response = ContactResponse(
            contact_id=contact_id,
            influencer_id=influencer.id,
            message=form.message.data,
            status=form.status.data,
            counter_offer=counter_offer
        )
        
        # Update contact status
        if form.status.data == 'accepted':
            contact.status = 'accepted'
        elif form.status.data == 'declined':
            contact.status = 'declined'
        elif form.status.data == 'counter_offer':
            contact.status = 'counter_offer'
        
        db.session.add(response)
        db.session.commit()
        
        flash('Response sent successfully!')
        return redirect(url_for('influencer_dashboard'))
    
    return render_template('respond_to_contact.html', form=form, contact=contact)

@app.route('/view-response/<int:contact_id>')
@login_required
def view_response(contact_id):
    contact = Contact.query.get_or_404(contact_id)
    
    # Check if user has permission to view this response
    if current_user.user_type == 'business':
        business = Business.query.filter_by(user_id=current_user.id).first()
        if contact.business_id != business.id:
            flash('You can only view responses to your own contacts')
            return redirect(url_for('business_dashboard'))
    elif current_user.user_type == 'influencer':
        influencer = Influencer.query.filter_by(user_id=current_user.id).first()
        if contact.influencer_id != influencer.id:
            flash('You can only view responses to your own contacts')
            return redirect(url_for('influencer_dashboard'))
    else:
        return redirect(url_for('index'))
    
    # Get the latest response for button logic
    latest_response = None
    if contact.responses:
        latest_response = max(contact.responses, key=lambda x: x.created_at)
    
    return render_template('view_response.html', contact=contact, latest_response=latest_response)

@app.route('/business-respond/<int:contact_id>', methods=['GET', 'POST'])
@login_required
def business_respond_to_counter(contact_id):
    if current_user.user_type != 'business':
        flash('Only businesses can respond to counter offers')
        return redirect(url_for('index'))
    
    contact = Contact.query.get_or_404(contact_id)
    business = Business.query.filter_by(user_id=current_user.id).first()
    
    # Check if this contact is from the current business
    if contact.business_id != business.id:
        flash('You can only respond to contacts from your business')
        return redirect(url_for('business_dashboard'))
    
    # Check if there's a counter offer to respond to
    latest_response = ContactResponse.query.filter_by(contact_id=contact_id).order_by(ContactResponse.created_at.desc()).first()
    if not latest_response or latest_response.status != 'counter_offer':
        flash('No counter offer to respond to')
        return redirect(url_for('business_dashboard'))
    
    # Check if business already responded to this counter offer
    existing_business_response = ContactResponse.query.filter_by(
        contact_id=contact_id, 
        business_id=business.id,
        status='business_counter'
    ).first()
    
    if existing_business_response:
        flash('You have already responded to this counter offer')
        return redirect(url_for('business_dashboard'))
    
    form = BusinessResponseForm()
    
    if form.validate_on_submit():
        counter_offer = None
        if form.status.data == 'business_counter':
            try:
                counter_offer = float(form.counter_offer.data) if form.counter_offer.data else None
            except:
                flash('Invalid counter offer amount')
                return render_template('business_respond.html', form=form, contact=contact, latest_response=latest_response)
        
        response = ContactResponse(
            contact_id=contact_id,
            business_id=business.id,
            influencer_id=contact.influencer_id,
            message=form.message.data,
            status=form.status.data,
            counter_offer=counter_offer
        )
        
        # Update contact status
        if form.status.data == 'accepted':
            contact.status = 'accepted'
        elif form.status.data == 'declined':
            contact.status = 'declined'
        elif form.status.data == 'business_counter':
            contact.status = 'business_counter'
        
        db.session.add(response)
        db.session.commit()
        
        flash('Response sent successfully!')
        return redirect(url_for('business_dashboard'))
    
    return render_template('business_respond.html', form=form, contact=contact, latest_response=latest_response)

# Review Routes
@app.route('/review/influencer/<int:influencer_id>', methods=['GET', 'POST'])
@login_required
def review_influencer(influencer_id):
    if current_user.user_type != 'business':
        flash('Only businesses can review influencers')
        return redirect(url_for('index'))
    
    influencer = Influencer.query.get_or_404(influencer_id)
    business = Business.query.filter_by(user_id=current_user.id).first()
    
    # Check if business already reviewed this influencer
    existing_review = Review.query.filter_by(
        reviewer_id=current_user.id,
        reviewed_influencer_id=influencer_id
    ).first()
    
    if existing_review:
        flash('You have already reviewed this influencer')
        return redirect(url_for('influencer_profile', id=influencer_id))
    
    form = ReviewForm()
    
    if form.validate_on_submit():
        review = Review(
            reviewer_id=current_user.id,
            reviewed_influencer_id=influencer_id,
            rating=form.rating.data,
            title=form.title.data,
            comment=form.comment.data
        )
        db.session.add(review)
        db.session.commit()
        
        flash('Review submitted successfully!')
        return redirect(url_for('influencer_profile', id=influencer_id))
    
    return render_template('review_influencer.html', form=form, influencer=influencer)

@app.route('/review/business/<int:business_id>', methods=['GET', 'POST'])
@login_required
def review_business(business_id):
    if current_user.user_type != 'influencer':
        flash('Only influencers can review businesses')
        return redirect(url_for('index'))
    
    business = Business.query.get_or_404(business_id)
    influencer = Influencer.query.filter_by(user_id=current_user.id).first()
    
    # Check if influencer already reviewed this business
    existing_review = Review.query.filter_by(
        reviewer_id=current_user.id,
        reviewed_business_id=business_id
    ).first()
    
    if existing_review:
        flash('You have already reviewed this business')
        return redirect(url_for('business_profile', id=business_id))
    
    form = ReviewForm()
    
    if form.validate_on_submit():
        review = Review(
            reviewer_id=current_user.id,
            reviewed_business_id=business_id,
            rating=form.rating.data,
            title=form.title.data,
            comment=form.comment.data
        )
        db.session.add(review)
        db.session.commit()
        
        flash('Review submitted successfully!')
        return redirect(url_for('business_profile', id=business_id))
    
    return render_template('review_business.html', form=form, business=business)

@app.route('/reviews/influencer/<int:influencer_id>')
def view_influencer_reviews(influencer_id):
    influencer = Influencer.query.get_or_404(influencer_id)
    reviews = Review.query.filter_by(reviewed_influencer_id=influencer_id).order_by(Review.created_at.desc()).all()
    
    # Calculate average rating
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    else:
        avg_rating = 0
    
    return render_template('view_influencer_reviews.html', influencer=influencer, reviews=reviews, avg_rating=avg_rating, total_reviews=len(reviews))

@app.route('/reviews/business/<int:business_id>')
def view_business_reviews(business_id):
    business = Business.query.get_or_404(business_id)
    reviews = Review.query.filter_by(reviewed_business_id=business_id).order_by(Review.created_at.desc()).all()
    
    # Calculate average rating
    if reviews:
        avg_rating = sum(review.rating for review in reviews) / len(reviews)
    else:
        avg_rating = 0
    
    return render_template('view_business_reviews.html', business=business, reviews=reviews, avg_rating=avg_rating, total_reviews=len(reviews))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True) 