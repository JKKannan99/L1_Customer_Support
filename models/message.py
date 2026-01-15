from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from db import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=False)

    sender = Column(String(50))  # 'Customer' or 'Agent'
    content = Column(Text, nullable=False)

    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
