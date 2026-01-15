# routes/agent_route.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from schemas.agent_schema import AgentLogin, AgentResponse
from services.agent_service import authenticate_agent, create_agent

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("/register", response_model=AgentResponse)
def register_agent(agent: AgentLogin, db: Session = Depends(get_db)):
    return create_agent(db, agent)

@router.post("/login")
def login_agent(agent: AgentLogin, db: Session = Depends(get_db)):
    return authenticate_agent(db, agent.username, agent.password)
