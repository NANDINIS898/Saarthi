# agents/sales_agents.py
from crewai import Agent, Task
from server.llm_api import get_groq_response

# Patch CrewAI to disable LLM globally (prevents any default OpenAI fallback)
import crewai
crewai.utilities.llm_utils._llm_via_environment_or_fallback = lambda *a, **kw: None

# Helper function to call Groq AI LLM
def sales_agent_llm(prompt: str) -> str:
    """
    Sends the prompt to Groq AI and returns the response.
    """
    return get_groq_response(prompt)

# CrewAI agent — orchestration only, no LLM
sales_agent = Agent(
    role="Sales Agent",
    goal="Negotiate loan terms and understand customer’s needs.",
    backstory=(
        "An experienced financial advisor helping customers choose the best loan "
        "amount, tenure, and rate suitable for their profile."
    ),
    llm=None  # <- IMPORTANT: disables CrewAI LLM
)
# Task definition (CrewAI uses this for orchestration, not LLM)
sales_task = Task(
    description="Discuss loan requirements such as amount, tenure, and purpose.",
    expected_output="Structured JSON with amount, tenure, purpose, and interest rate.",
    agent=sales_agent
)
