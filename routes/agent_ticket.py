from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.tickets import TicketStatus
from services.ticket_service import update_ticket_status

router = APIRouter(prefix="/agent", tags=["Agent"])

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
