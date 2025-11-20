from crewai import Crew
from agents.sales_agents import sales_agent, sales_task
from agents.verification_agent import verification_agent, verification_task, verify_customer
from agents.underwriting_agent import underwriting_agent, underwriting_task, evaluate_loan
from agents.sanction_agent import sanction_agent, sanction_task, generate_sanction_letter

class MasterOrchestrator:
    def __init__(self):
        self.crew = Crew(
            agents=[sales_agent, verification_agent, underwriting_agent, sanction_agent],
            tasks=[sales_task, verification_task, underwriting_task, sanction_task],
        )

    def start(self):
        print("🤖 Master Agent: Welcome to SmartLoan AI Assistant!\n")
        customer = input("Enter your name: ")

        # Step 1 - Sales Discussion
        amount = float(input("Desired loan amount (₹): "))
        tenure = int(input("Loan tenure (years): "))
        loan = {"name": customer, "amount": amount, "tenure": tenure, "interest": 10.0}

        # Step 2 - Verification
        kyc = verify_customer(customer)
        if kyc["status"] != "verified":
            print("❌ KYC verification failed. Exiting.")
            return

        # Step 3 - Underwriting
        decision = evaluate_loan(customer, amount, tenure)
        print(f"🧮 Decision: {decision}")

        # Step 4 - Sanction Letter (if approved)
        if decision["status"] == "approved":
            result = generate_sanction_letter(customer, loan, decision)
            print(f"📄 Sanction Letter Generated: {result['file']}")
        else:
            print("❌ Loan rejected or conditional.")

        print("\n✅ Workflow completed successfully.")

if __name__ == "__main__":
    orchestrator = MasterOrchestrator()
    orchestrator.start()
