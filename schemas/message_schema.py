from pydantic import BaseModel
from datetime import datetime

class MessageCreate(BaseModel):
    ticket_id: int
    sender: str
    content: str

class MessageResponse(BaseModel):
    sender: str
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True
