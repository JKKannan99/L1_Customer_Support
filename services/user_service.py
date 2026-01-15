from sqlalchemy.orm import Session
from models.users import User
from passlib.context import CryptContext
from jwt_utils.security import verify_password, create_access_token
from fastapi import HTTPException,status
from jwt_utils.XSS_sanitize import sanitize_text

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



def create_user(db: Session, user_data):
    existing_user=db.query(User).filter(
        User.email==user_data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="email already exist"
        )

    hashed_password = pass_context.hash(user_data.password)

    user = User(
        fullname=sanitize_text(user_data.fullname),
        email=user_data.email,
        password_hash=hashed_password  
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token({"sub": str(user.id),"role":"user"})

    return {
        "access_token": token,
        "token_type": "bearer"
    }