from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from auth import router as auth_router

app = FastAPI()

# Create tables
models.Base.metadata.create_all(bind=engine)

# CORS for frontend
origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth_router)

@app.get("/")
def home():
    return {"message": "FastAPI Backend Running!"}

