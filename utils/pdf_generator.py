from fpdf import FPDF

def generate_pdf(filename, name, loan, details):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Loan Sanction Letter", ln=True, align="C")
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Dear {name},", ln=True)
    pdf.cell(200, 10, txt=f"Your loan for ₹{loan['amount']} has been approved.", ln=True)
    pdf.cell(200, 10, txt=f"Tenure: {loan['tenure']} years at {loan['interest']}% interest.", ln=True)
    pdf.cell(200, 10, txt=f"Approval Type: {details.get('type', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt="Thank you for choosing SmartLoan AI.", ln=True)

    pdf.output(filename)
