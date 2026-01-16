from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from jwt_utils.dependencies import get_current_agent
from models.tickets import TicketStatus,Ticket
from services.ticket_service import update_ticket_status

router = APIRouter(prefix="/agent", tags=["Agent"])


@router.get("/tickets")
def get_all_tickets(
    db: Session = Depends(get_db),
    current_agent: dict = Depends(get_current_agent)
):
    return db.query(Ticket).order_by(Ticket.created_at.desc()).all()



@router.put("/tickets/{ticket_id}/status")
def change_ticket_status(
    ticket_id: int,
    status: TicketStatus,
    db: Session = Depends(get_db)
):
    ticket = update_ticket_status(db, ticket_id, status)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return {"message": "Ticket status updated", "status": ticket.status}
