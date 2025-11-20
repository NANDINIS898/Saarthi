from crewai import Agent, Task
from utils.credit_api import get_credit_score

underwriting_agent = Agent(
    role="Underwriting Agent",
    goal="Evaluate loan eligibility using credit score and salary logic.",
    backstory="A risk analyst who validates loan eligibility based on rules and credit data.",
)

underwriting_task = Task(
    description="Fetch credit score, check limits, and approve/reject loan as per eligibility.",
    expected_output="Decision: approved, conditional, or rejected, with reasons.",
    agent=underwriting_agent
)

def evaluate_loan(name, amount, tenure):
    credit_score = get_credit_score(name)
    pre_approved = 500000
    salary = 60000
    print(f"Credit Score for {name}: {credit_score}")

    if credit_score < 700:
        return {"status": "rejected", "reason": "Low credit score"}

    if amount <= pre_approved:
        return {"status": "approved", "type": "instant"}

    elif amount <= 2 * pre_approved:
        emi = (amount * (1 + 0.10)) / (tenure * 12)
        if emi <= 0.5 * salary:
            return {"status": "approved", "type": "salary_based", "emi": round(emi, 2)}
        else:
            return {"status": "rejected", "reason": "High EMI-to-salary ratio"}

    else:
        return {"status": "rejected", "reason": "Amount exceeds allowed limit"}
