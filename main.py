from fastapi import FastAPI
from routes.user_route import router as user_router
from routes.agent_route import router as agent_router

app = FastAPI()

app.include_router(user_router)

app.include_router(agent_router)

