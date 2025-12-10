# server/session_manager.py
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SessionManager:
    """
    Manages conversation sessions for the loan assistant.
    Stores conversation history and extracted information per session.
    """
    
    def __init__(self, session_timeout_minutes: int = 30):
        self.sessions: Dict[str, dict] = {}
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
    
    def create_session(self, user_id: Optional[str] = None) -> str:
        """Create a new conversation session"""
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {
            "session_id": session_id,
            "user_id": user_id,
            "conversation_history": [],
            "extracted_info": {
                "name": None,
                "amount": None,
                "tenure": None,
                "purpose": None,
                "income": None,
                "employment": None,
                "email": None,
                "phone": None
            },
            "workflow_triggered": False,
            "workflow_result": None,
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        }
        return session_id
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session data by ID"""
        session = self.sessions.get(session_id)
        if session:
            # Check if session has expired
            if datetime.now() - session["last_activity"] > self.session_timeout:
                self.delete_session(session_id)
                return None
            session["last_activity"] = datetime.now()
        return session
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to conversation history"""
        session = self.get_session(session_id)
        if session:
            session["conversation_history"].append({
                "role": role,
                "content": content,
                "timestamp": datetime.now().isoformat()
            })
    
    def update_extracted_info(self, session_id: str, info: dict):
        """Update extracted information for a session"""
        session = self.get_session(session_id)
        if session:
            for key, value in info.items():
                if value is not None and key in session["extracted_info"]:
                    session["extracted_info"][key] = value
    
    def get_conversation_history(self, session_id: str) -> List[dict]:
        """Get conversation history for a session"""
        session = self.get_session(session_id)
        return session["conversation_history"] if session else []
    
    def get_extracted_info(self, session_id: str) -> dict:
        """Get extracted information for a session"""
        session = self.get_session(session_id)
        return session["extracted_info"] if session else {}
    
    def is_info_complete(self, session_id: str) -> bool:
        """Check if minimum required information is collected"""
        info = self.get_extracted_info(session_id)
        # Minimum required: name, amount, tenure
        return bool(info.get("name") and info.get("amount") and info.get("tenure"))
    
    def mark_workflow_triggered(self, session_id: str, result: dict = None):
        """Mark that workflow has been triggered for this session"""
        session = self.get_session(session_id)
        if session:
            session["workflow_triggered"] = True
            if result:
                session["workflow_result"] = result
    
    def is_workflow_triggered(self, session_id: str) -> bool:
        """Check if workflow has been triggered"""
        session = self.get_session(session_id)
        return session["workflow_triggered"] if session else False
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def cleanup_expired_sessions(self):
        """Remove all expired sessions"""
        now = datetime.now()
        expired = [
            sid for sid, session in self.sessions.items()
            if now - session["last_activity"] > self.session_timeout
        ]
        for sid in expired:
            self.delete_session(sid)
    
    def get_missing_fields(self, session_id: str) -> List[str]:
        """Get list of missing required fields"""
        info = self.get_extracted_info(session_id)
        missing = []
        
        if not info.get("name"):
            missing.append("name")
        if not info.get("amount"):
            missing.append("loan amount")
        if not info.get("tenure"):
            missing.append("tenure (repayment period)")
        
        return missing


# Global session manager instance
session_manager = SessionManager()
