# utils/main.py

from agents.sales_agents import sales_agent, sales_task
from agents.verification_agent import verification_agent, verification_task, verify_customer
from agents.underwriting_agent import underwriting_agent, underwriting_task, evaluate_loan
from agents.sanction_agent import sanction_agent, sanction_task, generate_sanction_letter


class MasterOrchestrator:
    """
    Orchestrates the workflow for a loan assistant:
    Sales → Verification → Underwriting → Sanction.
    """

    def __init__(self):
        # If you later want to plug in CrewAI or other orchestration, you can.
        pass

    def run_workflow(self, user_data, user_message):
        """
        Executes the end-to-end workflow for a given user input.
        Returns a dictionary with all responses.
        """
        customer = user_data.get("name", "User")
        response_log = {"user": customer, "messages": []}

        # 1️⃣ Sales Agent Response
        sales_resp = f"Hello {customer}, I'm your Sales Agent! You said: '{user_message}'. Let's discuss your loan."
        response_log["messages"].append({"agent": "SalesAgent", "response": sales_resp})

        # 2️⃣ Verification
        kyc = verify_customer(customer)
        if kyc["status"] != "verified":
            fail_msg = "❌ KYC verification failed. Exiting workflow."
            response_log["messages"].append({"agent": "VerificationAgent", "response": fail_msg})
            return response_log

        response_log["messages"].append({"agent": "VerificationAgent", "response": "✅ KYC verified successfully."})

        # 3️⃣ Underwriting
        amount = user_data.get("amount", 100000)  # default for demo
        tenure = user_data.get("tenure", 5)       # default for demo
        decision = evaluate_loan(customer, amount, tenure)
        response_log["messages"].append({"agent": "UnderwritingAgent", "response": f"🧮 Decision: {decision}"})

        # 4️⃣ Sanction Letter
        if decision["status"] == "approved":
            loan_info = {"name": customer, "amount": amount, "tenure": tenure, "interest": 10.0}
            sanction = generate_sanction_letter(customer, loan_info, decision)
            response_log["messages"].append({"agent": "SanctionAgent", "response": f"📄 Sanction Letter Generated: {sanction['file']}"})
        else:
            response_log["messages"].append({"agent": "SanctionAgent", "response": "❌ Loan rejected or conditional."})

        return response_log


# Helper function for chat.py
def master_orchestration(user_data, user_message):
    orchestrator = MasterOrchestrator()
    workflow_response = orchestrator.run_workflow(user_data, user_message)

    # For chat endpoint, return only the last message of SalesAgent or combine all
    # Here, we'll return concatenated responses for demo
    combined_response = "\n".join([msg["response"] for msg in workflow_response["messages"]])
    return combined_response
