from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from schemas.ticket_schema import TicketCreate,TicketResponse
from services.ticket_service import create_ticket,get_all_tickets,get_user_tickets
from jwt_utils.dependencies import get_current_user,get_current_agent
from models.tickets import Ticket,TicketStatus

router = APIRouter(prefix="/user", tags=["Ticket"])

@router.post("/create-ticket")
async def create_ticket_api(
    category: str = Form(...),
    subject: str = Form(...),
    description: str = Form(...),
    callback_number: str = Form(None),
    screenshots: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)   #jwt fetching
):
    user_id = current_user["user_id"]

    if len(screenshots) == 0:
        raise HTTPException(
            status_code=400,
            detail="At least 1 screenshot is required"
        )

    data = TicketCreate(
        category=category,
        subject=subject,
        description=description,
        callback_number=callback_number
    )

    ticket = create_ticket(
        db=db,
        user_id=user_id,        # ✅ correct
        data=data,
        screenshots=screenshots
    )

    return {
        "message": "Ticket created successfully",
        "ticket_id": ticket.ticket_no
    }

@router.get("/tickets")
def get_all_ticket(db: Session = Depends(get_db)):
    return get_all_tickets(db)


@router.get("/my-tickets", response_model=List[TicketResponse])
def my_tickets(
    db: Session = Depends(get_db),
    current_user:dict = Depends(get_current_user)
):
    tickets = get_user_tickets(db,current_user["user_id"])
    return tickets

@router.post("/claim-ticket/{ticket_id}")
def claim_ticket(
    ticket_id: int,
    db: Session = Depends(get_db),
    current_agent: dict = Depends(get_current_agent)
):
    agent_id = current_agent["agent_id"]

    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket.agent_id is not None:
        raise HTTPException(status_code=400, detail="Ticket already claimed")

    ticket.agent_id = agent_id
    ticket.status = TicketStatus.in_progress

    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket claimed successfully",
        "ticket_id": ticket.ticket_no
    }
