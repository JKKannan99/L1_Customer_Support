# from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
# from datetime import datetime
# from db import Base

# class Ticket(Base):
#     __tablename__ = "tickets"
#     id = Column(String(50), primary_key=True)
#     subject = Column(String(200))
#     issue_type = Column(String(100))
#     status = Column(String(50), default="Open")
#     client_id = Column(String(50))
#     created_at = Column(DateTime, default=datetime.utcnow)

# class Message(Base):
#     __tablename__ = "messages"
#     id = Column(Integer, primary_key=True, index=True)
#     ticket_id = Column(String(50), ForeignKey("tickets.id"))
#     sender = Column(String(50)) # 'Customer' or 'Agent'
#     content = Column(Text)
#     timestamp = Column(DateTime, default=datetime.utcnow)


from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from db import Base

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(String(50), primary_key=True)
    subject = Column(String(200))
    type = Column(String(100)) # Changed from issue_type to type to match JS
    status = Column(String(50), default="Open")
    client_id = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String(50), ForeignKey("tickets.id"))
    sender = Column(String(50)) # 'Customer' or 'Agent'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)