from db import engine, Base
from models import users, agent, tickets, tkt_attachment,message

Base.metadata.create_all(bind=engine)  #for automatic table creation
