from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"   # your table name

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)   # hashed password

    # other fields later if needed (role, created_at, phone, etc)
