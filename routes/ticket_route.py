from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db import get_db
from schemas.ticket_schema import TicketCreate,TicketResponse
from services.ticket_service import create_ticket,get_all_tickets,get_user_tickets



router = APIRouter(prefix="/user", tags=["Ticket"])


@router.post("/create-ticket")
async def create_ticket_api(
    category: str = Form(...),
    subject: str = Form(...),
    description: str = Form(...),
    callback_number: str = Form(None),
    screenshots: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user_id: int = 1  # replace with JWT later
):
    if len(screenshots) < 3:
        raise HTTPException(
            status_code=400,
            detail="Minimum 3 screenshots are required"
        )

    data = TicketCreate(
        category=category,
        subject=subject,
        description=description,
        callback_number=callback_number
    )

    ticket = create_ticket(db, user_id, data, screenshots)  # ✅ matches service now
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
    user_id: int = 1  # replace with JWT later
):
    tickets = get_user_tickets(db, user_id)
    return tickets