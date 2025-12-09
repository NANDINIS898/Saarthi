import os
import sys

# Add project root (saarthi folder) to PYTHONPATH
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
sys.path.append(PROJECT_ROOT)

from utils.pdf_generator import generate_pdf

# Save inside test folder
output_path = os.path.join(CURRENT_DIR, "loan_letter_test.pdf")

generate_pdf(
    filename=output_path,
    name="Harshit Mittal",
    loan={
        "amount": "1,50,000",
        "tenure": "5",
        "interest": "7.5"
    },
    details={
        "type": "Instant Approval",
        "processing_fee": "₹999",
        "issue_date": "10 Dec 2025",
        "loan_id": "LN-2025-8842"
    }
)

print(f"PDF generated successfully at: {output_path}")
