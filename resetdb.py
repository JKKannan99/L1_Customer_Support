from db import engine, Base
from models.models import Ticket, Message

def reset():
    print("Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("Creating new tables with correct columns...")
    Base.metadata.create_all(bind=engine)
    print("Database reset successfully! Now run seed_db.py again.")

if __name__ == "__main__":
    reset()