from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from db import get_db
from schemas.users_schema import UserCreate,LoginRequest
from services.user_service import authenticate_user
from services.user_service import create_user
from models.users import User

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    return create_user(db, user)
   
   
@router.post("/login")
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    return authenticate_user(db, data.email, data.password)   
