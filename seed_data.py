import random
from datetime import datetime

from app import app, db, User, Influencer, Business, generate_password_hash


def random_choice(list_) :
    return random.choice(list_)


def seed_influencers(target=30):
    categories = [
        'technology', 'fashion', 'food', 'fitness', 'travel', 'lifestyle',
        'gaming', 'education', 'entertainment', 'business'
    ]
    locations = ['Mumbai', 'Delhi', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata']
    platforms = ['Instagram', 'YouTube', 'Twitter', 'Facebook', 'Tiktok']
    sample_bios = [
        'Passionate creator focused on genuine storytelling.',
        'Lifestyle and travel enthusiast sharing honest reviews.',
        'Tech reviewer and gadget lover.',
        'Food blogger exploring local flavours and recipes.',
        'Fitness coach sharing routines and healthy tips.'
    ]

    existing = Influencer.query.count()
    to_create = max(0, target - existing)
    print(f'Existing influencers: {existing}. Creating {to_create}.')
    # Real Indian names list to use for influencers
    indian_names = [
        'Aarav Sharma', 'Aditya Verma', 'Arjun Kapoor', 'Aryan Patel', 'Ayaan Singh',
        'Dev Malhotra', 'Dhruv Mehta', 'Isha Rao', 'Kavya Nair', 'Priya Joshi',
        'Sneha Gupta', 'Ananya Reddy', 'Rohan Sinha', 'Rohit Kumar', 'Karan Bhattacharya',
        'Nikhil Chawla', 'Parth Desai', 'Rahul Iyer', 'Rajesh Menon', 'Kabir Khan',
        'Tanvi Sharma', 'Megha Pillai', 'Sanya Ghosh', 'Aditi Nair', 'Vikram Bhat',
        'Sameer Shah', 'Shreya Rao', 'Anjali Kapoor', 'Neha Gupta', 'Kunal Verma'
    ]

    # Prepare names for creation (if needing more than list length, names will repeat)
    names_pool = []
    while len(names_pool) < to_create:
        names_pool.extend(indian_names)
    names_pool = names_pool[:to_create]

    for i in range(to_create):
        idx = existing + i + 1
        email = f'influencer{idx}@example.com'
        # create a user
        user = User(email=email, password_hash=generate_password_hash('password'), user_type='influencer')
        db.session.add(user)
        db.session.flush()

        name = names_pool[i]
        cats = random_choice(categories)
        loc = random_choice(locations)
        bio = random_choice(sample_bios)
        followers = random.randint(1000, 500000)
        engagement = round(random.uniform(0.5, 12.0), 2)
        plats = ','.join(random.sample(platforms, k=random.randint(1, 3)))
        rate = round(random.uniform(100.0, 10000.0), 2)

        influencer = Influencer(
            user_id=user.id,
            name=name,
            categories=cats,
            location=loc,
            bio=bio,
            followers_count=followers,
            engagement_rate=engagement,
            platforms=plats,
            rate_per_post=rate,
            portfolio_url=f'https://example.com/{email}'
        )
        db.session.add(influencer)

    db.session.commit()
    print('Finished seeding influencers')


def seed_businesses(target=20):
    business_types = [
        'technology', 'fashion', 'food', 'fitness', 'travel', 'finance', 'education', 'entertainment', 'automotive', 'real_estate'
    ]
    locations = ['Mumbai', 'Delhi', 'Bengaluru', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata']
    sample_desc = [
        'We build scalable web products.',
        'Local fashion brand focused on sustainable materials.',
        'Organic food subscription service.',
        'Fitness studio with a digital-first approach.',
        'Travel agency specialising in curated experiences.'
    ]

    existing = Business.query.count()
    to_create = max(0, target - existing)
    print(f'Existing businesses: {existing}. Creating {to_create}.')

    # Realistic Indian business names and contacts
    business_names = [
        'AshaTech Solutions', 'Prana Fashion House', 'Swaad Organic Foods', 'FitCore Studio', 'Yatra Trails',
        'Nivesh Capital', 'EduGrow Academy', 'Rangmanch Productions', 'DriveWell Automotive', 'HomeSpace Realtors',
        'Zenith Labs', 'Kala Couture', 'Chai & Co', 'Pulse Fitness Club', 'ExploreMore Travels',
        'Lakshmi Finance', 'BrightPath Learning', 'StageLight Media', 'AutoMitra Services', 'Haven Properties'
    ]

    contact_names = [
        'Rohit Sharma', 'Priya Menon', 'Suresh Kumar', 'Anita Desai', 'Vikram Joshi',
        'Meera Nair', 'Arun Patel', 'Kavita Singh', 'Nitin Gupta', 'Simran Kaur',
        'Anil Verma', 'Pooja Shah', 'Rajat Iyer', 'Deepa Rao', 'Karan Mehta',
        'Sneha Bose', 'Manish Kapoor', 'Rhea Thomas', 'Siddharth Rao', 'Aisha Khan'
    ]

    # Prepare pools
    names_pool = []
    contacts_pool = []
    while len(names_pool) < to_create:
        names_pool.extend(business_names)
    while len(contacts_pool) < to_create:
        contacts_pool.extend(contact_names)
    names_pool = names_pool[:to_create]
    contacts_pool = contacts_pool[:to_create]

    for i in range(to_create):
        idx = existing + i + 1
        email = f'business{idx}@example.com'
        user = User(email=email, password_hash=generate_password_hash('password'), user_type='business')
        db.session.add(user)
        db.session.flush()

        company_name = names_pool[i]
        btype = random_choice(business_types)
        loc = random_choice(locations)
        desc = random_choice(sample_desc)
        contact = contacts_pool[i]
        phone = f'+91{random.randint(6000000000, 9999999999)}'
        # create a simple slug for website
        slug = company_name.lower().replace(' ', '')
        website = f'https://{slug}.example.com'

        business = Business(
            user_id=user.id,
            company_name=company_name,
            business_type=btype,
            location=loc,
            description=desc,
            contact_person=contact,
            phone=phone,
            website=website
        )
        db.session.add(business)

    db.session.commit()
    print('Finished seeding businesses')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_influencers(30)
        seed_businesses(20)
        print('Seeding complete')
