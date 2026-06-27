from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.user import User
from app.schemas.user import UserCreate
# Assuming a get_db dependency exists
# from app.db.session import get_db

router = APIRouter()

@router.post("/register")
def register(user_in: UserCreate, db: Session = Depends(lambda: None)): # Placeholder for get_db
    hashed_password = get_password_hash(user_in.password)
    user = User(email=user_in.email, hashed_password=hashed_password)
    # db.add(user)
    # db.commit()
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user_in: UserCreate, db: Session = Depends(lambda: None)): # Placeholder for get_db
    # user = db.query(User).filter(User.email == user_in.email).first()
    # if not user or not verify_password(user_in.password, user.hashed_password):
    #     raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token = create_access_token(subject=user_in.email)
    return {"access_token": access_token, "token_type": "bearer"}
