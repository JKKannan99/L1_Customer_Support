# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker

# # Change 'password' to your MySQL password. Create a database named 'support_db' in MySQL first.
# URL_DATABASE = "mysql+pymysql://root:admin@localhost:3306/support_db"

# engine = create_engine(URL_DATABASE)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Update 'admin' to your actual MySQL password if it's different
# Ensure the database 'support_db' is already created in your MySQL server
URL_DATABASE = "mysql+pymysql://root:Admin123@localhost:3306/support_db"

engine = create_engine(
    URL_DATABASE, 
    pool_pre_ping=True,  # Checks connection health before use
    pool_recycle=3600    # Re-connects every hour to prevent timeouts
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def run_manual_seed():
    from models.models import Ticket # Local import to avoid circular dependency
    db = SessionLocal()
    # Adding logic here to insert a ticket...
    # (Same logic as Option 1)
    db.close()