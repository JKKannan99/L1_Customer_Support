from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base
import enum


class TicketCategory(str, enum.Enum):
    payment = "Payment Issue"
    network = "Network Issue"
    other = "Other"

class TicketStatus(str, enum.Enum):
    open = "Open"
    in_progress = "In Progress"
    closed = "Closed"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    ticket_no = Column(String(20), unique=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)

    category = Column(Enum(TicketCategory), nullable=False)
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    callback_number = Column(String(15))

    status = Column(Enum(TicketStatus), default=TicketStatus.open,nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="tickets")
    agent = relationship("Agent", back_populates="tickets")
    attachments = relationship(
        "TicketAttachment",
        back_populates="ticket",
        cascade="all, delete-orphan"
    )
    messages = relationship(
    "Message",
    backref="ticket",
    cascade="all, delete-orphan"
)


