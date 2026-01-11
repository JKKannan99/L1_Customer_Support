from db import engine, Base
from models import users, agent, tickets, tkt_attachment

Base.metadata.create_all(bind=engine)
