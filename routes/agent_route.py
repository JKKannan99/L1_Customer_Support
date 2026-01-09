from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db import get_db
from schemas.agent_schema import AgentLogin, AgentResponse
from services.agent_service import authenticate_agent

router = APIRouter(prefix="/agent", tags=["Agent"])

@router.post("/login", response_model=AgentResponse)
def agent_login(data: AgentLogin, db: Session = Depends(get_db)):
    agent = authenticate_agent(db, data.username, data.password)

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return {
        "id": agent.id,
        "username": agent.username,
        "message": "Agent login successful"
    }
