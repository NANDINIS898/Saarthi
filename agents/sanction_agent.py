from crewai import Agent, Task
from utils.pdf_generator import generate_pdf
from server.llm_api import get_groq_response

# Patch CrewAI to disable LLM globally (prevents any default OpenAI fallback)
import crewai
crewai.utilities.llm_utils._llm_via_environment_or_fallback = lambda *a, **kw: None

def sanction_agent_llm(prompt: str):
    return get_groq_response(prompt)


sanction_agent = Agent(
    role="Sanction Letter Generator",
    goal="Generate automated PDF sanction letters for approved loans.",
    backstory="A document automation specialist that prepares sanction letters.",
    llm=None
)

sanction_task = Task(
    description="Generate a sanction letter PDF for approved loans.",
    expected_output="Sanction letter file path or confirmation message.",
    agent=sanction_agent
)

def generate_sanction_letter(name, loan, decision):
    filename = f"{name}_SanctionLetter.pdf"
    generate_pdf(filename, name, loan, decision)
    return {"status": "success", "file": filename}
