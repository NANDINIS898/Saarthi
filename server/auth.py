from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import SignupModel, LoginModel, UserResponse
from models import User
from utils import hash_password, verify_password, create_access_token, SECRET_KEY, ALGORITHM
from database import get_db, SessionLocal
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -------- SIGNUP --------
MAX_PW_LEN = 72

@router.post("/signup")
def signup(user: SignupModel, db: Session = Depends(get_db)):
    if len(user.password.encode('utf-8')) > MAX_PW_LEN:
        raise HTTPException(status_code=400, detail="Password too long. Max 72 characters allowed.")

    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = hash_password(user.password)  # truncate just in case
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


# -------- AUTH DEPENDENCY --------
def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# -------- PROFILE (Protected) --------
@router.get("/profile", response_model=UserResponse)
def profile(current_user: User = Depends(get_current_user)):
    return current_user
