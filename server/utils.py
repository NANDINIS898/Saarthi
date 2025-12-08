from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

def hash_password(password: str):
    # encode password to bytes
    password_bytes = password.encode("utf-8")
    # truncate to 72 bytes (bcrypt limit)
    truncated = password_bytes[:72]
    # pass bytes directly to passlib
    return pwd_context.hash(truncated)


MAX_PW_LEN = 72

def verify_password(plain, hashed):
    truncated = plain.encode("utf-8")[:MAX_PW_LEN]
    return pwd_context.verify(truncated, hashed)


def create_access_token(data: dict, expires_minutes=60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
