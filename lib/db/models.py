from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from datetime import datetime
import os

# Get the current directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Create the database path
DATABASE_PATH = os.path.join(BASE_DIR, 'cli-project-event-management.db')
# Create database URL
DATABASE_URL = f'sqlite:///{DATABASE_PATH}'

Base = declarative_base()

# Junction Tables
event_attendees = Table(
    'event_attendees',
    Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('attendee_id', Integer, ForeignKey('attendees.id'), primary_key=True)
)

event_vendors = Table(
    'event_vendors',
    Base.metadata,
    Column('event_id', Integer, ForeignKey('events.id'), primary_key=True),
    Column('vendor_id', Integer, ForeignKey('vendors.id'), primary_key=True)
)

class Event(Base):
    __tablename__ = 'events'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)
    location = Column(String)
    budget = Column(Float)
    status = Column(String)
    description = Column(String)
    
    attendees = relationship("Attendee", secondary=event_attendees, back_populates="events")
    vendors = relationship("Vendor", secondary=event_vendors, back_populates="events")

    def __repr__(self):
        return f"<Event {self.name}>"

class Attendee(Base):
    __tablename__ = 'attendees'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)
    rsvp_status = Column(String)
    dietary_preferences = Column(String)
    
    events = relationship("Event", secondary=event_attendees, back_populates="attendees")

    def __repr__(self):
        return f"<Attendee {self.name}>"

class Vendor(Base):
    __tablename__ = 'vendors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    service_type = Column(String)
    contact_info = Column(String)
    rate = Column(Float)
    rating = Column(Integer)
    
    events = relationship("Event", secondary=event_vendors, back_populates="vendors")

    def __repr__(self):
        return f"<Vendor {self.name}>"

# Create engine
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Create all tables
def init_db():
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    init_db()