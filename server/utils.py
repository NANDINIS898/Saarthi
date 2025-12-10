import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

MAX_PW_LEN = 72  # bcrypt limit in bytes

security = HTTPBearer()

def hash_password(password: str):
    truncated_bytes = password.encode("utf-8")[:MAX_PW_LEN]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(truncated_bytes, salt)
    return hashed.decode("utf-8")

def verify_password(plain: str, hashed: str):
    truncated_bytes = plain.encode("utf-8")[:MAX_PW_LEN]
    hashed_bytes = hashed.encode("utf-8")
    return bcrypt.checkpw(truncated_bytes, hashed_bytes)

def create_access_token(data: dict, expires_minutes=60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user_id