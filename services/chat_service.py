# from sqlalchemy.orm import Session
# from models.models import Ticket, Message

# def get_user_tickets(db: Session, client_id: str):
#     return db.query(Ticket).filter(Ticket.client_id == client_id).all()

# def get_all_tickets(db: Session):
#     return db.query(Ticket).all()

# # def save_message(db: Session, ticket_id: str, sender: str, content: str):
# #     msg = Message(ticket_id=ticket_id, sender=sender, content=content)
# #     db.add(msg)
# #     db.commit()
# #     return msg

# # In services/chat_service.py
# def save_message(db: Session, ticket_id: str, sender: str, content: str):
#     # Print this to your console to see what is failing
#     print(f"Saving message: Ticket:{ticket_id}, Sender:{sender}, Content:{content}")
#     new_msg = Message(ticket_id=ticket_id, sender=sender, content=content)
#     db.add(new_msg)
#     db.commit()

# def get_messages(db: Session, ticket_id: str):
#     return db.query(Message).filter(Message.ticket_id == ticket_id).all()

from sqlalchemy.orm import Session
from models.models import Ticket, Message

def get_user_tickets(db: Session, client_id: str):
    return db.query(Ticket).filter(Ticket.client_id == client_id).all()

def get_all_tickets(db: Session):
    return db.query(Ticket).all()

def save_message(db: Session, ticket_id: str, sender: str, content: str):
    new_msg = Message(ticket_id=ticket_id, sender=sender, content=content)
    db.add(new_msg)
    db.commit()
    db.refresh(new_msg)
    return new_msg

def get_messages(db: Session, ticket_id: str):
    return db.query(Message).filter(Message.ticket_id == ticket_id).order_by(Message.timestamp).all()

from db import SessionLocal
from models.models import Ticket

def seed():
    db = SessionLocal()
    # Check if we already have this ticket to avoid duplicates
    exists = db.query(Ticket).filter(Ticket.id == "TKT-101").first()
    if not exists:
        test_ticket = Ticket(
            id="TKT-101",
            subject="Order not delivered",
            type="Delivery Issue",
            status="Open",
            client_id="Kannan"
        )
        db.add(test_ticket)
        db.commit()
        print("Test ticket created successfully!")
    else:
        print("Test ticket already exists.")
    db.close()

if __name__ == "__main__":
    seed()