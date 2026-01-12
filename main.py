# from fastapi import FastAPI
# from fastapi.staticfiles import StaticFiles
# from db import engine, Base
# from routes.chat_routes import router as chat_router

# Base.metadata.create_all(bind=engine) # Creates MySQL tables

# app = FastAPI()
# app.include_router(chat_router)
# app.mount("/static", StaticFiles(directory="static"), name="static")

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from db import engine, Base
from routes.chat_routes import router as chat_router

# Creates MySQL tables automatically
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)

# Mount static files (CSS/JS)
app.mount("/static", StaticFiles(directory="static"), name="static")
# Mount templates as static if you aren't using a template engine (Jinja2)
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

@app.get("/")
def read_root():
    return {"message": "Support System API is running"}