from models import init_db, Base, engine

print("Creating database tables...")
Base.metadata.drop_all(engine)  # Drop existing tables
Base.metadata.create_all(engine)  # Create new tables
print("Database tables created successfully!")
