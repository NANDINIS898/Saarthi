from crewai import Agent, Task
from utils.crm_mock import get_customer_details

verification_agent = Agent(
    role="Verification Agent",
    goal="Verify customer identity and KYC details using CRM data.",
    backstory="An assistant responsible for validating customer KYC and contact information.",
)

verification_task = Task(
    description="Fetch KYC details (phone, address) from dummy CRM for the provided customer.",
    expected_output="Verification result: verified or failed, with CRM details if found.",
    agent=verification_agent
)

def verify_customer(name: str):
    details = get_customer_details(name)
    if details:
        return {"status": "verified", "details": details}
    return {"status": "failed"}
