from sqlalchemy.orm import Session
from models.message import Message

def save_message(db: Session, ticket_id: int, sender: str, content: str):
    message = Message(
        ticket_id=ticket_id,
        sender=sender,
        content=content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message
