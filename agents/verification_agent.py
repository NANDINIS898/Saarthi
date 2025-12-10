from crewai import Agent, Task
from utils.crm_mock import get_customer_details
from server.llm_api import get_groq_response

# Patch CrewAI to disable LLM globally (prevents any default OpenAI fallback)
import crewai
crewai.utilities.llm_utils._llm_via_environment_or_fallback = lambda *a, **kw: None

def verification_agent_llm(prompt: str):
    """Wrapper to call Groq API from verification agent."""
    return get_groq_response(prompt)

# Create Verification Agent with required backstory
verification_agent = Agent(
    role="Verification Agent",
    goal="Verify KYC and customer info",
    backstory=(
        "Responsible for verifying customer identity, KYC documents, and loan eligibility "
        "by asking structured questions and validating customer info from CRM."
    ),
    llm=None  # disables CrewAI's default LLM
)

# Create a Task for the agent
verification_task = Task(
    description="Fetch KYC details (phone, address) from dummy CRM for the provided customer.",
    expected_output="Verification result: verified or failed, with CRM details if found.",
    agent=verification_agent
)

# Helper function for verification logic
def verify_customer(name: str):
    details = get_customer_details(name)
    if details:
        return {"status": "verified", "details": details}
    return {"status": "failed"}
