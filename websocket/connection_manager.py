from typing import Dict, List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, ticket_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(ticket_id, []).append(websocket)

    def disconnect(self, ticket_id: int, websocket: WebSocket):
        self.active_connections[ticket_id].remove(websocket)

    async def broadcast(self, ticket_id: int, message: dict):
        for connection in self.active_connections.get(ticket_id, []):
            await connection.send_json(message)
