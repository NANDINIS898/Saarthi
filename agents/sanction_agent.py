from crewai import Agent, Task
from utils.pdf_generator import generate_pdf

sanction_agent = Agent(
    role="Sanction Letter Generator",
    goal="Generate automated PDF sanction letters for approved loans.",
    backstory="A document automation specialist that prepares sanction letters.",
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
