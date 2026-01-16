from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from models.tickets import TicketCategory,TicketStatus

class TicketCreate(BaseModel):
    category:TicketCategory
    subject: str
    description: str
    callback_number:str

class AttachmentResponse(BaseModel):
    file_path:str
    file_type:str

class TicketResponse(BaseModel):
    ticket_no: str
    category: TicketCategory
    subject: str
    description: str
    callback_number: str | None
    status: TicketStatus
    created_at: datetime
    agent_id: Optional[int]
    attachments:list[AttachmentResponse]=[]

    class Config:
        from_attributes = True