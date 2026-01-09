from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from db import engine

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    fullname = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))   

Base.metadata.create_all(bind=engine)
