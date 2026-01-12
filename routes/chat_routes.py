# from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
# from sqlalchemy.orm import Session
# from db import get_db
# from services import chat_service as service
# import json

# router = APIRouter()

# # Simple manager to track who is chatting in which ticket
# # class ConnectionManager:
# #     def __init__(self):
# #         self.active_connections: dict = {}

# #     async def connect(self, websocket: WebSocket, ticket_id: str):
# #         await websocket.accept()
# #         if ticket_id not in self.active_connections:
# #             self.active_connections[ticket_id] = []
# #         self.active_connections[ticket_id].append(websocket)

# #     def disconnect(self, websocket: WebSocket, ticket_id: str):
# #         self.active_connections[ticket_id].remove(websocket)

# #     async def broadcast(self, message: dict, ticket_id: str):
# #         if ticket_id in self.active_connections:
# #             for connection in self.active_connections[ticket_id]:
# #                 await connection.send_text(json.dumps(message))

# # manager = ConnectionManager()

# from typing import List, Dict
# from fastapi import WebSocket

# class ConnectionManager:
#     def __init__(self):
#         # Dictionary to store connections per ticket: { "ticket_id": [WebSocket1, WebSocket2] }
#         self.active_connections: Dict[str, List[WebSocket]] = {}

#     async def connect(self, websocket: WebSocket, ticket_id: str):
#         await websocket.accept()
#         if ticket_id not in self.active_connections:
#             self.active_connections[ticket_id] = []
#         self.active_connections[ticket_id].append(websocket)

#     def disconnect(self, websocket: WebSocket, ticket_id: str):
#         if ticket_id in self.active_connections:
#             self.active_connections[ticket_id].remove(websocket)

#     async def broadcast(self, message: dict, ticket_id: str):
#         # Send message to EVERYONE connected to this specific ticket room
#         if ticket_id in self.active_connections:
#             for connection in self.active_connections[ticket_id]:
#                 await connection.send_json(message)

# manager = ConnectionManager()

# @router.get("/api/tickets/{client_id}")
# def read_tickets(client_id: str, db: Session = Depends(get_db)):
#     return service.get_user_tickets(db, client_id)

# @router.get("/api/all-tickets")
# def read_all(db: Session = Depends(get_db)):
#     return service.get_all_tickets(db)

# # @router.websocket("/ws/chat/{ticket_id}/{sender}")
# # async def websocket_chat(websocket: WebSocket, ticket_id: str, sender: str, db: Session = Depends(get_db)):
# #     await manager.connect(websocket, ticket_id)
# #     try:
# #         while True:
# #             data = await websocket.receive_text()
# #             service.save_message(db, ticket_id, sender, data) # Save to DB
# #             await manager.broadcast({"sender": sender, "message": data}, ticket_id)
# #     except WebSocketDisconnect:
# #         manager.disconnect(websocket, ticket_id)

# @router.websocket("/ws/chat/{ticket_id}/{sender}")
# async def websocket_chat(websocket: WebSocket, ticket_id: str, sender: str, db: Session = Depends(get_db)):
#     await manager.connect(websocket, ticket_id)
#     try:
#         while True:
#             data = await websocket.receive_text()
            
#             # 1. Create message object for broadcasting
#             chat_msg = {"sender": sender, "message": data}
            
#             # 2. Save to DB (Handle errors so the chat doesn't freeze)
#             try:
#                 # Ensure 'sender' matches your DB ENUM ('Customer' or 'Agent') 
#                 service.save_message(db, ticket_id, sender, data)
#             except Exception as e:
#                 print(f"DB Save Error: {e}")

#             # 3. Broadcast to both Agent and Customer in the room
#             await manager.broadcast(chat_msg, ticket_id)
            
#     except WebSocketDisconnect:
#         manager.disconnect(websocket, ticket_id)

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from db import get_db
import services.chat_service as service
from typing import List, Dict
import json
router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, ticket_id: str):
        await websocket.accept()
        if ticket_id not in self.active_connections:
            self.active_connections[ticket_id] = []
        self.active_connections[ticket_id].append(websocket)

    def disconnect(self, websocket: WebSocket, ticket_id: str):
        if ticket_id in self.active_connections:
            self.active_connections[ticket_id].remove(websocket)

    async def broadcast(self, message: dict, ticket_id: str):
        if ticket_id in self.active_connections:
            for connection in self.active_connections[ticket_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@router.get("/api/tickets/{client_id}")
def read_tickets(client_id: str, db: Session = Depends(get_db)):
    return service.get_user_tickets(db, client_id)

@router.get("/api/all-tickets")
def read_all(db: Session = Depends(get_db)):
    return service.get_all_tickets(db)

@router.get("/api/messages/{ticket_id}")
def get_chat_history(ticket_id: str, db: Session = Depends(get_db)):
    return service.get_messages(db, ticket_id)

# @router.websocket("/ws/chat/{ticket_id}/{sender}")
# async def websocket_chat(websocket: WebSocket, ticket_id: str, sender: str, db: Session = Depends(get_db)):
#     await manager.connect(websocket, ticket_id)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             service.save_message(db, ticket_id, sender, data)
#             await manager.broadcast({"sender": sender, "message": data}, ticket_id)
#     except WebSocketDisconnect:
#         manager.disconnect(websocket, ticket_id)


@router.websocket("/ws/chat/{ticket_id}/{sender}")
async def websocket_chat(websocket: WebSocket, ticket_id: str, sender: str, db: Session = Depends(get_db)):
    await manager.connect(websocket, ticket_id)
    try:
        while True:
            # 1. Receive the raw text from the frontend
            raw_data = await websocket.receive_text()
            
            # 2. Extract the actual text content
            try:
                # Try to parse it as JSON (for Agent messages)
                parsed_json = json.loads(raw_data)
                clean_message = parsed_json.get("message", raw_data)
            except json.JSONDecodeError:
                # If it's not JSON (like some Customer messages), use it as is
                clean_message = raw_data

            # 3. Save ONLY the clean text to the database
            service.save_message(db, ticket_id, sender, clean_message)
            
            # 4. Broadcast a clean dictionary to all participants
            # This ensures both Agent and Customer receive a structured JSON object
            await manager.broadcast({"sender": sender, "message": clean_message}, ticket_id)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, ticket_id)