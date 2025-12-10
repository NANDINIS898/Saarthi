from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.database import engine
import server.models
from server.auth import router as auth_router
from server.chat import router as chat_router
from server.document_upload import router as doc_router
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

# Create tables
server.models.Base.metadata.create_all(bind=engine)

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
app.include_router(chat_router, prefix="/api")
app.include_router(doc_router, prefix="/api")

@app.get("/")
def home():
    return {"message": "FastAPI Backend Running!"}

