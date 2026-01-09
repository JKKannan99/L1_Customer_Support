from sqlalchemy.orm import Session
from models.agent import Agent

def authenticate_agent(db: Session, username: str, password: str):
    agent = db.query(Agent).filter(
        Agent.username == username,
        Agent.password == password,
        Agent.is_active == True
    ).first()

    return agent
