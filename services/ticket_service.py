import os
from datetime import datetime,timezone
from fastapi import UploadFile
from sqlalchemy.orm import Session
from models.tickets import Ticket, TicketStatus
from models.tkt_attachment import TicketAttachment
from schemas.ticket_schema import TicketCreate

UPLOAD_FOLDER = "uploads"

def create_ticket(db: Session, user_id: int, data: TicketCreate, screenshots: list[UploadFile]):

    # ✅ Ensure upload directory exists
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    ticket = Ticket(
        user_id=user_id,
        category=data.category,
        subject=data.subject,
        description=data.description,
        callback_number=data.callback_number,
        status=TicketStatus.open
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    # Generate ticket number
    ticket.ticket_no = f"TKT-{ticket.id:03d}"
    db.commit()
    db.refresh(ticket)

    # Save screenshots
    for file in screenshots:
        filename = f"{ticket.ticket_no}_{datetime.now(timezone.utc).timestamp()}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        with open(filepath, "wb") as f:
            f.write(file.file.read())

        attachment = TicketAttachment(
            ticket_id=ticket.id,
            file_path=filepath,
            file_type=file.content_type
        )
        db.add(attachment)

    db.commit()
    return ticket


def get_all_tickets(db: Session):
    return db.query(Ticket).all()


def get_user_tickets(db: Session, user_id: int):
    return (
        db.query(Ticket)
        .filter(Ticket.user_id == user_id)
        .order_by(Ticket.created_at.desc())
        .all()
    )


def update_ticket_status(db: Session, ticket_id: int, status: TicketStatus):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        return None

    ticket.status = status
    db.commit()
    db.refresh(ticket)
    return ticket