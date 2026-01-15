# services/agent_service.py
from sqlalchemy.orm import Session
from models.agent import Agent
from passlib.context import CryptContext
from jwt_utils.security import verify_password, create_access_token
from fastapi import HTTPException, status

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_agent(db: Session, agent_data):
    # hash password
    hashed_password = pass_context.hash(agent_data.password)

    # check if username exists
    existing_agent = db.query(Agent).filter(Agent.username == agent_data.username).first()
    if existing_agent:
        raise HTTPException(status_code=400, detail="Username already exists")

    agent = Agent(
        username=agent_data.username,
        password=hashed_password,
        is_active=True
    )

    db.add(agent)
    db.commit()
    db.refresh(agent)
    return {
        "id": agent.id,
        "username": agent.username,
        "message": "Agent created successfully"
    }


def authenticate_agent(db: Session, username: str, password: str):
    agent = db.query(Agent).filter(
        Agent.username == username,
        Agent.is_active == True
    ).first()

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    if not verify_password(password, agent.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    token = create_access_token({"sub": str(agent.id), "role": "agent"})

    return {
        "access_token": token,
        "token_type": "bearer"
    }
