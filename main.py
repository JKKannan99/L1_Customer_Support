from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
#from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from routes.user_route import router as user_router
from routes.agent_route import router as agent_router
from routes.ticket_route import router as ticket_router
from routes import agent_ticket,message_ws
app = FastAPI()



# CORS CONFIG
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",   # Live Server
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/uploads",StaticFiles(directory="uploads"),name="uploads")



app.include_router(user_router)
app.include_router(agent_router)
app.include_router(ticket_router)
app.include_router(message_ws.router)
app.include_router(agent_ticket.router)
