# from db import SessionLocal
# from models.models import Ticket

# def seed():
#     db = SessionLocal()
#     # Check if we already have this ticket to avoid duplicates
#     exists = db.query(Ticket).filter(Ticket.id == "TKT-101").first()
#     if not exists:
#         test_ticket = Ticket(
#             id="TKT-101",
#             subject="Order not delivered",
#             type="Delivery Issue",
#             status="Open",
#             client_id="Kannan"
#         )
#         db.add(test_ticket)
#         db.commit()
#         print("Test ticket created successfully!")
#     else:
#         print("Test ticket already exists.")
#     db.close()

# if __name__ == "__main__":
#     seed()

from db import SessionLocal
from models.models import Ticket

def seed():
    db = SessionLocal()
    # Force a new ticket if the table was reset
    test_ticket = Ticket(
        id="TKT-101",
        subject="Payment Failed",
        type="Billing",
        status="Open",
        client_id="Kannan"
    )
    db.add(test_ticket)
    db.commit()
    print("Test ticket added successfully!")
    db.close()

seed()