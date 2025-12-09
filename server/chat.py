import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from server.llm_api import get_groq_response
from utils.main import master_orchestration

router = APIRouter()

# -----------------------------
# Request Model
# -----------------------------
class ChatRequest(BaseModel):
    message: str
    name: str | None = None
    email: str | None = None
    amount: float | None = None
    tenure: int | None = None

# -----------------------------
# Chat Endpoint
# -----------------------------
@router.post("/chat")
async def chat(req: ChatRequest):
    # Prepare user data from request
    user_data = {
        "name": req.name or "Demo User",
        "email": req.email or "demo@example.com",
        "amount": req.amount or 100000,
        "tenure": req.tenure or 5,
    }

    try:
        # Call master orchestration to get agent responses
        workflow_response = master_orchestration(user_data, req.message)

        # Optional: also get LLM response via Groq
        llm_prompt = f"Sales Agent: Respond as a helpful loan assistant. User says: {req.message}"
        llm_response = get_groq_response(llm_prompt)

        # Combine all responses nicely
        final_response = {
            "workflow_responses": workflow_response.split("\n"),
            "llm_response": llm_response or None
        }

        return final_response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
