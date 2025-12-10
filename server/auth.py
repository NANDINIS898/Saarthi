from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from server.schemas import SignupModel, LoginModel, UserResponse
from server.models import User
from server.utils import (
    hash_password, 
    verify_password, 
    create_access_token, 
    get_current_user_id,
    MAX_PW_LEN
)
from server.database import get_db

router = APIRouter()

# -------- SIGNUP --------
@router.post("/signup")
def signup(user: SignupModel, db: Session = Depends(get_db)):
    if len(user.password) > MAX_PW_LEN:
        raise HTTPException(status_code=400, detail=f"Password too long. Max {MAX_PW_LEN} characters allowed.")

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed_pw)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Signup successful!", "user_id": new_user.id}


# -------- LOGIN --------
@router.post("/login")
def login(user: LoginModel, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": db_user.id})

    return {"access_token": token, "user": db_user}


# -------- PROFILE --------
@router.get("/profile", response_model=UserResponse)
def get_profile(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user