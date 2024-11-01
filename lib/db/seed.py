from faker import Faker
from models import Base, Event, Attendee, Vendor, engine, Session
from datetime import datetime, timedelta
import random

fake = Faker()

def seed_data():
    # Clear existing data
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    session = Session()
    
    # Create vendors
    vendor_types = ['catering', 'decoration', 'music', 'photography', 'venue']
    vendors = []
    for _ in range(10):
        vendor = Vendor(
            name=fake.company(),
            service_type=random.choice(vendor_types),
            contact_info=fake.email(),
            rate=random.uniform(500, 5000),
            rating=random.randint(1, 5)
        )
        vendors.append(vendor)
    session.add_all(vendors)
    
    # Create attendees
    attendees = []
    for _ in range(50):
        attendee = Attendee(
            name=fake.name(),
            email=fake.email(),
            phone=fake.phone_number(),
            rsvp_status=random.choice(['pending', 'confirmed', 'declined']),
            dietary_preferences=random.choice(['none', 'vegetarian', 'vegan', 'gluten-free'])
        )
        attendees.append(attendee)
    session.add_all(attendees)
    
    # Create events
    event_statuses = ['planning', 'ongoing', 'completed']
    events = []
    for _ in range(5):
        event = Event(
            name=fake.company() + " " + random.choice(['Conference', 'Wedding', 'Birthday', 'Meeting']),
            date=fake.date_time_between(start_date='now', end_date='+1y'),
            location=fake.address(),
            budget=random.uniform(5000, 50000),
            status=random.choice(event_statuses),
            description=fake.text(),
            attendees=random.sample(attendees, random.randint(5, 20)),
            vendors=random.sample(vendors, random.randint(2, 5))
        )
        events.append(event)
    session.add_all(events)
    
    session.commit()
    session.close()

if __name__ == '__main__':
    print("🌱 Seeding database...")
    seed_data()
    print("✅ Done seeding!")