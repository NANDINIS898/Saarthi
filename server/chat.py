import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from server.llm_api import get_conversational_response
from server.session_manager import session_manager
from utils.info_extractor import extract_information_from_conversation
from utils.conversation_prompts import (
    SYSTEM_PROMPT, 
    APPROVAL_MESSAGE_TEMPLATE,
    REJECTION_MESSAGE_TEMPLATE,
    CONFIRMATION_TEMPLATE,
    MISSING_INFO_TEMPLATE
)
from agents.verification_agent import verify_customer
from agents.underwriting_agent import evaluate_loan
from agents.sanction_agent import generate_sanction_letter
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# -----------------------------
# Request Model
# -----------------------------
class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

# -----------------------------
# Chat Endpoint
# -----------------------------
@router.post("/chat")
async def chat(req: ChatRequest):
    try:
        # Get or create session
        if req.session_id:
            session = session_manager.get_session(req.session_id)
            if not session:
                # Session expired, create new one
                session_id = session_manager.create_session()
            else:
                session_id = req.session_id
        else:
            session_id = session_manager.create_session()
        
        # Add user message to conversation history
        session_manager.add_message(session_id, "user", req.message)
        
        # Get conversation history
        conversation_history = session_manager.get_conversation_history(session_id)
        
        # Extract information from conversation (with error handling)
        try:
            extracted_info = extract_information_from_conversation(conversation_history)
            if extracted_info:
                session_manager.update_extracted_info(session_id, extracted_info)
        except Exception as e:
            print(f"Info extraction error: {e}")
            # Continue without extraction
        
        # Check if workflow should be triggered
        should_trigger_workflow = (
            session_manager.is_info_complete(session_id) and 
            not session_manager.is_workflow_triggered(session_id)
        )
        
        if should_trigger_workflow:
            # Get extracted information
            info = session_manager.get_extracted_info(session_id)
            
            try:
                # Run workflow
                workflow_result = run_loan_workflow(info)
                session_manager.mark_workflow_triggered(session_id, workflow_result)
                
                # Generate workflow response
                assistant_response = generate_workflow_response(info, workflow_result)
            except Exception as e:
                print(f"Workflow error: {e}")
                assistant_response = "I encountered an issue processing your loan application. Let me try again."
        else:
            # Generate conversational response
            try:
                assistant_response = get_conversational_response(
                    conversation_history,
                    SYSTEM_PROMPT
                )
            except Exception as e:
                print(f"LLM error: {e}")
                assistant_response = "I'm having trouble connecting. Could you please try again?"
        
        # Add assistant response to conversation history
        session_manager.add_message(session_id, "assistant", assistant_response)
        
        # Return response
        return {
            "response": assistant_response,
            "session_id": session_id,
            "extracted_info": session_manager.get_extracted_info(session_id),
            "workflow_triggered": session_manager.is_workflow_triggered(session_id),
        }
    
    except Exception as e:
        print(f"Chat error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


def run_loan_workflow(info: dict) -> dict:
    """
    Run the loan approval workflow with extracted information.
    """
    result = {
        "verification": None,
        "underwriting": None,
        "sanction": None,
        "final_status": "pending"
    }
    
    # Step 1: Verification
    kyc_result = verify_customer(info.get("name", "Unknown"))
    result["verification"] = kyc_result
    
    if kyc_result.get("status") != "verified":
        result["final_status"] = "rejected"
        result["rejection_reason"] = "KYC verification failed"
        return result
    
    # Step 2: Underwriting
    underwriting_result = evaluate_loan(
        info.get("name"),
        info.get("amount", 100000),
        info.get("tenure", 5)
    )
    result["underwriting"] = underwriting_result
    
    if underwriting_result.get("status") == "approved":
        # Step 3: Generate sanction letter
        loan_info = {
            "name": info.get("name"),
            "amount": info.get("amount"),
            "tenure": info.get("tenure"),
            "interest": 10.0
        }
        sanction_result = generate_sanction_letter(
            info.get("name"),
            loan_info,
            underwriting_result
        )
        result["sanction"] = sanction_result
        result["final_status"] = "approved"
    else:
        result["final_status"] = "rejected"
        result["rejection_reason"] = underwriting_result.get("reason", "Eligibility criteria not met")
    
    return result


def generate_workflow_response(info: dict, workflow_result: dict) -> str:
    """
    Generate a human-friendly response based on workflow result.
    """
    name = info.get("name", "there")
    amount = info.get("amount", 0)
    tenure = info.get("tenure", 0)
    
    if workflow_result["final_status"] == "approved":
        # Calculate EMI
        principal = amount
        rate = 10.0 / 100 / 12
        tenure_months = tenure * 12
        emi = principal * rate * (1 + rate)**tenure_months / ((1 + rate)**tenure_months - 1)
        
        return APPROVAL_MESSAGE_TEMPLATE.format(
            name=name,
            amount=amount,
            tenure=tenure,
            interest=10.0,
            emi=int(emi)
        )
    else:
        reason = workflow_result.get("rejection_reason", "eligibility criteria")
        return REJECTION_MESSAGE_TEMPLATE.format(
            name=name,
            amount=amount,
            reason=reason
        )
