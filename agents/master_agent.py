from crewai import Crew  # optional
from utils.main import MasterOrchestrator




def master_orchestration(user_data, user_message):
    """
    This function bridges FastAPI with the CrewAI orchestration logic.
    It simulates the Sales Agent interaction as part of the workflow.
    """
    try:
        orchestrator = MasterOrchestrator()
        
        # Instead of using console input, inject user_data dynamically
        customer = user_data.get("name", "User")
        print(f"🧠 Running Master Orchestrator for {customer}")

        # Simulate a conversation entry point (Sales Agent discussion)
        response = f"Hello {customer}, I'm your Sales Agent Saarthi! You said: '{user_message}'. Let's discuss your loan details."

        # TODO: you can later enhance this to:
        #  1. Run sales_agent logic directly (via CrewAI)
        #  2. Trigger downstream agents conditionally (verification → underwriting → sanction)

        return response
    
    except Exception as e:
        print("Error in master orchestration:", e)
        return "Something went wrong in orchestration."
