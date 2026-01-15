from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from models.message import Message
from schemas.message_schema import MessageResponse

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.get("/{ticket_id}", response_model=List[MessageResponse])
def get_ticket_messages(ticket_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Message)
        .filter(Message.ticket_id == ticket_id)
        .order_by(Message.timestamp)
        .all()
    )
