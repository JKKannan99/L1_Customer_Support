from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.user_route import router as user_router
from routes.agent_route import router as agent_router
from routes.ticket_route import router as ticket_router
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

app.include_router(user_router)

app.include_router(agent_router)

app.include_router(ticket_router)

