from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from db import get_db
from websocket.connection_manager import ConnectionManager
from services.message_service import save_message
from models.tickets import Ticket

router = APIRouter()
manager = ConnectionManager()

@router.websocket("/ws/tickets/{ticket_no}")
async def ticket_chat(
    websocket: WebSocket,
    ticket_no: str,
    db: Session = Depends(get_db)
):
    # 🔍 Find ticket using ticket_no
    ticket = db.query(Ticket).filter(Ticket.ticket_no == ticket_no).first()

    if not ticket:
        # Close connection if ticket not found
        await websocket.close(code=1008)
        return

    ticket_id = ticket.id
    await manager.connect(ticket_id, websocket)
    print("WebSocket connected for ticket:", ticket_no)

    try:
        while True:
            data = await websocket.receive_json()
            print("Received:", data)

            sender = data["sender"]
            content = data["content"]

            message = save_message(db, ticket_id, sender, content)

            await manager.broadcast(ticket_id, {
                "sender": message.sender,
                "content": message.content,
                "timestamp": message.timestamp.isoformat()
            })

    except WebSocketDisconnect:
        manager.disconnect(ticket_id, websocket)
        print("WebSocket disconnected:", ticket_no)
