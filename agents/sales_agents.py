from crewai import Agent, Task

sales_agent = Agent(
    role="Sales Agent",
    goal="Negotiate loan terms and understand customer’s needs.",
    backstory=(
        "An experienced financial advisor helping customers choose the best loan "
        "amount, tenure, and rate suitable for their profile."
    ),
)

sales_task = Task(
    description="Discuss loan requirements such as amount, tenure, and purpose.",
    expected_output="Structured JSON with amount, tenure, purpose, and interest rate.",
    agent=sales_agent
)
